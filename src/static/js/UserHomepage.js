let compatibility = Object.keys(components)
    .filter(key => ['processor', 'motherboard', 'RAM', 'videocard', 'computer_case'].includes(key))
    .reduce((acc, key) => {
        if (key == 'processor'){
            acc[key] = components[key].map(item => {
                return {
                    processor_id: item.processor_id,
                    motherboard: 1,
                    videocard: 1,
                    RAM: 1,
                    computer_case: 1
                };
            });
        } else if (key == 'motherboard'){
            acc[key] = components[key].map(item => {
                return {
                    motherboard_id: item.motherboard_id,
                    processor: 1,
                    videocard: 1,
                    RAM: 1,
                    computer_case: 1
                };
            });
        } else if (key == 'RAM'){
            acc[key] = components[key].map(item => {
                return {
                    RAM_id: item.RAM_id,
                    motherboard: 1,
                    videocard: 1,
                    processor: 1,
                    computer_case: 1
                };
            });
        } else if (key == 'videocard'){
            acc[key] = components[key].map(item => {
                return {
                    videocard_id: item.videocard_id,
                    motherboard: 1,
                    processor: 1,
                    RAM: 1,
                    computer_case: 1
                };
            });
        } else if (key == 'computer_case'){
            acc[key] = components[key].map(item => {
                return {
                    computer_case_id: item.computer_case_id,
                    motherboard: 1,
                    videocard: 1,
                    RAM: 1,
                    processor: 1
                };
            });
        }
        return acc;
    }, {})

let totalCost = 0;
let order = {}

Object.keys(components).forEach(key => {
    order[key] = undefined;
})

let group_param_names = {
    computer_case: 'manufacturer',
    cooler: 'type',
    HDD: 'capacity',
    motherboard: 'manufacturer',
    power_block: 'power',
    RAM: 'manufacturer',
    SSD: 'capacity',
    videocard: 'manufacturer',
    processor: 'manufacturer'
}

const descriptions = Object.keys(components).reduce((acc, key) => {
    acc[key] = components[key].map(item => {
        const description = Object.entries(item)
            .filter(([itemKey]) => itemKey !== key + '_id' && itemKey !== 'price')
            .map(([itemKey, value]) => `${itemKey}: ${value}`)
            .join('\n'); 
        
        return {
            id: item[key + '_id'],
            description: description
        };
    });
    return acc;
}, {})

function showOptions(componentName, Drop) {
    const select = document.getElementById(componentName); 
    const optionsDiv = document.getElementById(`${componentName}-options`);
    const selectedValue = select.value; 

    if (Drop){

        const previouslySelected = optionsDiv.querySelector('input[type="radio"]:checked');
        if (previouslySelected) {
            previouslySelected.checked = false;
            updateTotal(); 
            dropCompatibility(componentName)
            order[componentName] = undefined
            toogleCreateButton()
        }
        
    }

    if (!selectedValue) {
        optionsDiv.style.display = 'none';
        return;
    }
    

    const component_list = components[componentName]; 
    optionsDiv.innerHTML = component_list
    .filter(component => ((component[group_param_names[componentName]] == selectedValue) && (checkCompatibility(componentName, component[componentName + '_id']))))
    .map((component, index) => `
        <div class="radio-option">
            <input type="radio" name="${componentName}" id="${componentName}-${index}" 
                   value="${component.price}" 
                   ${order[componentName] == component[componentName + '_id'] ? 'checked' : ''} 
                   onclick="(() => { 
                        updateTotal(); 
                        updateOrder('${componentName}', '${component[componentName + '_id']}'); 
                        toogleCreateButton(); 
                        updateCompatibility('${componentName}', '${component[componentName + '_id']}'); 
                    })()"
            <label for="${componentName}-${index}">${names[componentName].find(item => item[componentName + '_id'] == component[componentName + '_id']).name} - $${component.price}</label>
            <button class="info-btn" onclick="toggleTooltip(this)">i</button>
            <div class="tooltip">${descriptions[componentName].find(item => item.id == component[componentName + '_id']).description}</div>
        </div>
    `).join('');

    optionsDiv.style.display = 'block';
}

function updateOrder(componentName, componentId){
    order[componentName] = componentId
}

function toggleTooltip(button) {
    
    document.querySelectorAll('.tooltip').forEach(tooltip => {
        tooltip.classList.remove('active');
    });
    
    
    const tooltip = button.nextElementSibling;
    tooltip.classList.toggle('active');
    
    
    document.addEventListener('click', function closeTooltip(e) {
        if (!button.contains(e.target) && !tooltip.contains(e.target)) {
            tooltip.classList.remove('active');
            document.removeEventListener('click', closeTooltip);
        }
    });
}

function updateTotal() {
    totalCost = 0;
    document.querySelectorAll('input[type="radio"]:checked').forEach(radio => {
        totalCost += parseInt(radio.value);
    });
    document.querySelector('.total-cost').textContent = `Total: $${totalCost}`;
}

function updateCompatibility(componentName, componentId) {
    if (componentName === 'cooler' || componentName === 'power_block' || componentName === 'SSD' || componentName === 'HDD') {
        return;
    }

    Object.keys(compatibility).filter(item => item !== componentName).forEach(component => {
        compatibility[component].forEach(record => {
            record[componentName] = 1;
        });
    });

    const url = `/api/${componentName}?id=${encodeURIComponent(componentId)}`;

    let data;
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.send(null);

    data = JSON.parse(xhr.responseText);


    Object.keys(data).forEach(component => {
        compatibility[component].forEach(record => {
            if (!data[component].includes(record[`${component}_id`])) {
                record[componentName] = 0;
            }
        });
    });

    Object.keys(data).forEach(component => showOptions(component, false));
}


function dropCompatibility(componentName){
    if (componentName == 'cooler' || componentName == 'power_block' || componentName == 'SSD' || componentName == 'HDD'){
        return;
    }
    Object.keys(compatibility).filter(item => item !== componentName).forEach(component => {
        compatibility[component].forEach(record => {
            record[componentName] = 1;
        });
    });
    Object.keys(compatibility).forEach(component => showOptions(component, false))
}

function checkCompatibility(componentName, componentId){
    if (componentName == 'cooler' || componentName == 'power_block' || componentName == 'SSD' || componentName == 'HDD'){
        return true
    }
    
    const compatibilities = compatibility[componentName].find(item => item[componentName + '_id'] == componentId)

    if (componentName == 'processor'){
        if (compatibilities.motherboard == 1 && compatibilities.computer_case == 1 && compatibilities.RAM == 1 && compatibilities.videocard == 1){
            return true;
        }
        return false;
    } else if (componentName == 'motherboard'){
        if (compatibilities.processor == 1 && compatibilities.computer_case == 1 && compatibilities.RAM == 1 && compatibilities.videocard == 1){
            return true;
        }
        return false;
    } else if (componentName == 'videocard'){
        if (compatibilities.motherboard == 1 && compatibilities.computer_case == 1 && compatibilities.RAM == 1 && compatibilities.processor == 1){
            return true;
        }
        return false;
    } else if (componentName == 'RAM'){
        if (compatibilities.motherboard == 1 && compatibilities.computer_case == 1 && compatibilities.processor == 1 && compatibilities.videocard == 1){
            return true;
        }
        return false;
    } else if (componentName == 'computer_case'){
        if (compatibilities.motherboard == 1 && compatibilities.processor == 1 && compatibilities.RAM == 1 && compatibilities.videocard == 1){
            return true;
        }
        return false;
    }
}

function setOrder(){
    save_order_sync();
    sessionStorage.setItem('order', JSON.stringify(order));
    const costs = Object.keys(order).reduce((prices, componentName) => {
        prices[componentName] = components[componentName].find(item => item[`${componentName}_id`] === order[componentName]).price;
        return prices;
    }, {});
    sessionStorage.setItem('costs', JSON.stringify(costs));
    const orderNames = Object.keys(order).reduce((orderNames, componentName) => {
        orderNames[componentName] = names[componentName].find(item => item[componentName + '_id'] == order[componentName]).name;
        return orderNames;
    }, {});
    sessionStorage.setItem('names', JSON.stringify(orderNames));
}

function save_order_sync() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/user/saveorder", false); // false — синхронный режим
    xhr.setRequestHeader("Content-Type", "application/json");
    try {
        xhr.send(JSON.stringify(order));
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log("Заказ сохранён:", response);
        } else {
            console.error("Ошибка при сохранении заказа:", xhr.statusText);
            return null;
        }
    } catch (err) {
        console.error("Ошибка при отправке запроса:", err);
        return null;
    }
}

function orderIsFull(){
    return Object.values(order).every(item => item !== undefined);
}

function toogleCreateButton(){
    const createBtn = document.querySelector('.create-order-btn');
    if (orderIsFull()){
        createBtn.classList.add('active');
        createBtn.disabled = false;
    } else{
        createBtn.classList.remove('active');
        createBtn.disabled = true;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    restoreOrderFromServer();
});

function restoreOrderFromServer() {
    for (const componentName in draft_order) {
        if (draft_order[componentName] !== null) {
            order[componentName] = draft_order[componentName];

            const selectedComponent = components[componentName].find(item => item[componentName + '_id'] == draft_order[componentName]);

            if (selectedComponent) {
                const groupValue = selectedComponent[group_param_names[componentName]];
                
                const selectEl = document.getElementById(componentName);
                selectEl.value = groupValue;

                showOptions(componentName, false);

                const radio = document.querySelector(`input[name="${componentName}"][value="${selectedComponent.price}"]`);
                if (radio) {
                    radio.checked = true;
                }

                updateCompatibility(componentName, order[componentName]);
                updateOrder(componentName, order[componentName]);
            }
        }
    }

    updateTotal();
    toogleCreateButton();
}