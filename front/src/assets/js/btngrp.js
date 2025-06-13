function get_time_data(date) {
    const today = new Date();
    // 将传入的日期字符串转换为日期对象  
    const targetDate = new Date(date);
    const timeDifference = targetDate - today;
    const dayDifference = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));
    const daynum = dayDifference - 3;
    $.ajax({
        url: '{% url "get_Charts" %}',
        method: "post",
        dataType: "text",
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            'date': date
        },
        success: function (data) {
            data = JSON.parse(data).timesep;
            max_resnum = data.max_resnum.if_valid;
            if_valid = data
            for (let j = 0; j < 24; j++) {
                const hourKey = `hour_${j}`; // 生成字段名，例如 hour_0, hour_1, ...  
                const checkbox = document.getElementById(`btncheck${daynum}-${j + 1}`); // 获取对应的 checkbox  

                if (data[hourKey] === true) {
                    checkbox.checked = true; // 设置为选中状态  
                } else {
                    checkbox.checked = false; // 设置为未选中状态  
                }
            }
        }
    })
};

const today = new Date(); // 获取当前日期  

// 计算未来日期  
const futureDates = [
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 3), // 三天后  
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 4), // 四天后  
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 5),  // 五天后  
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 6),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 8),
    new Date(today.getFullYear(), today.getMonth(), today.getDate() + 9),
];

const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
const formattedDates = futureDates.map(date => date.toLocaleDateString('zh-CN', options));

// 将格式化后的日期设置到相应的元素中  
formattedDates.forEach((dateString, index) => {
    const dayOfWeek = new Date(futureDates[index]).toLocaleDateString('zh-CN', { weekday: 'long' }); // 获取星期几  
    document.getElementById(`mcr-date${index}`).innerText = `${dateString}日 - ${dayOfWeek}`;
});

for (let i = 0; i < 7; i++) {
    const container = document.getElementById(`mar-manage${i}`);
    if (container) {
        // 创建要插入的内容  
        container.innerHTML = `  
                    <div class="col-lg-5 text-start">  
                        <input type="checkbox" class="btn-check" id="checkdate${i}" autocomplete="off">  
                        <label class="btn btn-outline-danger" for="checkdate${i}">将当日设为不可用</label>  
                    </div>  
                    <div style="padding-right:6px" class="col-lg-2 align-middle xmin-mcr text-end">选择预约时段：</div>  
                    <div class="col-lg-auto text-end btn-group" role="group" aria-label="Basic checkbox toggle button group">  
                        <input type="radio" class="btn-check" name="timeint${i}" id="timeint${i}-1" autocomplete="off" onchange="updateButtonAvailability(${i}, 2)">  
                        <label class="btn btn-outline-info" for="timeint${i}-1">2小时</label>  

                        <input type="radio" class="btn-check" name="timeint${i}" id="timeint${i}-2" autocomplete="off" onchange="updateButtonAvailability(${i}, 3)">  
                        <label class="btn btn-outline-info" for="timeint${i}-2">3小时</label>  

                        <input type="radio" class="btn-check" name="timeint${i}" id="timeint${i}-3" autocomplete="off" onchange="updateButtonAvailability(${i}, 4)">  
                        <label class="btn btn-outline-info" for="timeint${i}-3">4小时</label>  
                    </div>  
                    <div class="col-lg-2 text-end btn-group"  role="group" aria-label="Basic checkbox toggle button group">
                        <select class="form-select" id="mcr-select${i}" aria-label="Default select example">
                            <option value="0" selected>选择最多预约数</option>
                            <option value="1">最多预约：10</option>
                            <option value="2">最多预约：50</option>
                            <option value="3">最多预约：100</option>
                            <option value="4">最多预约：无限制</option>
                        </select>
                    </div>
                `;
    }
}


const containers = [
    document.getElementById('mcr-manage'),
    document.getElementById('mcr-manage0'),
    document.getElementById('mcr-manage1'),
    document.getElementById('mcr-manage2'),
    document.getElementById('mcr-manage3'),
    document.getElementById('mcr-manage4'),
    document.getElementById('mcr-manage5'),
    document.getElementById('mcr-manage6')
];

for (let s = 0; s < containers.length; s++) {
    const container = containers[s];
    for (let j = 0; j < 24; j++) {
        const wrapper = document.createElement('div');
        wrapper.className = 'checkbox-wrapper';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = `btn-check btn-${s}`;
        checkbox.id = `btncheck${s}-${j + 1}`;
        checkbox.autocomplete = 'off';

        const label = document.createElement('label');
        label.className = 'btn btn-outline-primary';
        label.setAttribute('for', checkbox.id);
        label.innerText = (j < 10) ? `○ - 0${j}:00 ->` : `○ - ${j}:00 ->`;

        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);
        container.appendChild(wrapper);

        // 添加事件监听器  
        checkbox.addEventListener('change', function () {
            handleCheckboxChange(checkbox, s, j);
        });
    }
}


//按钮组基本选中事件
function handleCheckboxChange(checkbox, groupIndex, buttonIndex) {
    const container = containers[groupIndex];
    const buttons = container.querySelectorAll('input[type="checkbox"]'); // 这是按钮组  
    const i = 4; // 设定i的值，根据上下文，选择需要的数量  

    // 定义需要检查的范围  
    const previousStart = Math.max(0, buttonIndex - (i - 1));
    const subsequentEnd = Math.min(buttons.length, buttonIndex + (i - 1));

    // 检查前面和后续的按钮状态  
    const previousButtons = [...buttons].slice(previousStart, buttonIndex);
    const subsequentButtons = [...buttons].slice(buttonIndex + 1, subsequentEnd);

    const previousChecked = previousButtons.some(btn => btn.checked);
    const subsequentChecked = subsequentButtons.some(btn => btn.checked);

    const findClosestChecked_pre = (btns) => {  // 前方按钮  
        for (let index = buttonIndex - 1; index >= 0; index--) {
            if (btns[index].checked) {
                return btns[index];
            }
        }
        return null;
    };

    const findClosestChecked_nxt = (btns) => {  // 后续按钮  
        for (let index = buttonIndex + 1; index < btns.length; index++) {
            if (btns[index].checked) {
                return btns[index];
            }
        }
        return null;
    };

    // 处理按钮被选中  
    if (checkbox.checked) {
        checkbox.nextElementSibling.className = 'btn btn-outline-primary';
        // 找到后续的最近被选中的按钮  
        const closestCheckedNxt = findClosestChecked_nxt(buttons);

        // 如果后续有被选中的按钮  
        if (closestCheckedNxt) {
            const closestIndex = [...buttons].indexOf(closestCheckedNxt);
            // 计算有效的上限  
            const upperLimit = Math.min(closestIndex, buttonIndex + i);
            for (let k = buttonIndex + 1; k < upperLimit; k++) {
                buttons[k].nextElementSibling.className = 'btn btn-warning'; // 设置样式为btn-outline-warning  
            }
        } else {
            // 如果没有被选中的按钮，则将x后面i - 1个按钮样式设为btn-outline-warning  
            for (let k = buttonIndex + 1; k <= Math.min(buttons.length - 1, buttonIndex + (i - 1)); k++) {
                buttons[k].nextElementSibling.className = 'btn btn-warning'; // 设置样式为btn-outline-warning  
            }
        }
    } else { // 处理按钮被解除选中  
        // 找到后续的最近被选中的按钮  
        const closestCheckedNxt = findClosestChecked_nxt(buttons);

        // 如果后续有被选中的按钮  
        if (closestCheckedNxt) {
            const closestIndex = [...buttons].indexOf(closestCheckedNxt);
            // 恢复x之后到closestCheckedNxt之前的按钮样式  
            for (let k = buttonIndex + 1; k < closestIndex; k++) {
                buttons[k].nextElementSibling.className = 'btn btn-outline-primary'; // 恢复样式  
            }
        } else {
            // 如果没有被选中的按钮，则恢复x后面i - 1个按钮样式  
            for (let k = buttonIndex + 1; k <= Math.min(buttons.length - 1, buttonIndex + (i - 1)); k++) {
                buttons[k].nextElementSibling.className = 'btn btn-outline-primary'; // 恢复样式  
            }
        }

        // 检查按钮前面是否有被选中按钮  
        const closestCheckedPre = findClosestChecked_pre(buttons);
        if (closestCheckedPre) {
            const closestIndex = [...buttons].indexOf(closestCheckedPre);
            // 将closestCheckedPre之后i - 1个按钮样式统一设置为btn-outline-warning  
            for (let k = closestIndex + 1; k <= Math.min(buttons.length - 1, closestIndex + (i - 1)); k++) {
                if (!buttons[k].checked) {
                    buttons[k].nextElementSibling.className = 'btn btn-warning'; // 设置样式为btn-outline-warning  
                }
            }
        }
    }
}

//根据是否可用选项决定按钮组是否可用
function toggleButtons(i) {
    // 获取复选框的选中状态  
    const checkbox = document.getElementById(`checkdate${i}`);
    const isChecked = checkbox.checked;

    // 获取按钮组  
    const buttonGroup = document.getElementById(`mcr-manage${i}`);

    // 获取按钮组中的所有按钮  
    const buttons = buttonGroup.querySelectorAll('button');

    // 根据复选框的状态，设置按钮的禁用状态  
    buttons.forEach(button => {
        if (isChecked) {
            if (!button.disabled) {
                button.classList.add('disabled');
                button.setAttribute('disabled', true);
            }
        } else {
            if (button.disabled) {
                button.classList.remove('disabled');
                button.removeAttribute('disabled');
            }
        }
    });
};


//根据选中时段长度决定禁用的按钮
function updateButtonAvailability(i, selectedHours) {
    // 获取按钮组  
    const buttonGroup = document.getElementById(`mcr-manage${i}`);
    const buttons = buttonGroup.querySelectorAll('button');

    // 根据选中的小时数禁用相应数量的按钮  
    const buttonsToDisable = selectedHours - 1; // 计算需要禁用的按钮数量  

    buttons.forEach((button, index) => {
        if (index >= buttons.length - buttonsToDisable) {
            if (!button.disabled) {
                button.classList.add('disabled');
                button.setAttribute('disabled', true);
            }
        } else {
            if (button.disabled) {
                button.classList.remove('disabled');
                button.removeAttribute('disabled');
            }
        }
    });
};