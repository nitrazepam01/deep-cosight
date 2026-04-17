/**
 * Custom Select Component - 自定义下拉选择组件
 * 替代原生 select 元素，提供完全定制的样式支持
 * 
 * @param {HTMLElement|string} container - 容器元素或选择器
 * @param {Object} options - 配置选项
 * @param {string} options.placeholder - 占位符文本
 * @param {boolean} options.multiple - 是否多选
 * @param {boolean} options.searchable - 是否可搜索
 * @param {boolean} options.expandUp - 是否向上展开（默认向下）
 * @param {number} options.maxVisibleItems - 最大可见选项数量（超过时显示滚动条）
 * @param {Array} options.items - 选项列表
 * @param {Function} options.onChange - 值变化回调
 */

class CustomSelect {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' ? document.querySelector(container) : container;
        if (!this.container) {
            console.error('CustomSelect: container not found');
            return;
        }

        this.options = {
            placeholder: options.placeholder || '请选择',
            multiple: options.multiple || false,
            searchable: options.searchable || false,
            expandUp: options.expandUp || false,  // 是否向上展开
            maxVisibleItems: options.maxVisibleItems !== undefined ? options.maxVisibleItems : 6,  // 最大可见选项数，默认为 6
            onChange: options.onChange || null,
            ...options
        };

        this.isOpen = false;
        this.selectedValues = this.options.multiple ? (options.selectedValues !== undefined ? options.selectedValues : []) : (options.selectedValue !== undefined ? options.selectedValue : null);
        this.items = options.items || [];
        this.closeTimeout = null;
        this.boundHandlers = {};
        
        this.init();
    }

    init() {
        this.render();
        this.bindEvents();
    }

    render() {
        const selectedItems = this.items.filter(item => 
            this.options.multiple 
                ? this.selectedValues.includes(item.value)
                : item.value === this.selectedValues
        );

        const displayText = this.getDisplayText(selectedItems);

        // 根据 expandUp 选项设置方向类名
        const directionClass = this.options.expandUp ? 'custom-select-dropup' : 'custom-select-dropdown';

        this.container.innerHTML = `
            <div class="custom-select-wrapper">
                <div class="custom-select-display" tabindex="0">
                    <span class="custom-select-display-text">${displayText}</span>
                    <i class="custom-select-arrow fas fa-chevron-${this.options.expandUp ? 'up' : 'down'}"></i>
                </div>
                <div class="custom-select-dropdown ${directionClass}" style="--max-visible-items: ${this.options.maxVisibleItems};">
                    ${this.options.searchable ? `
                        <div class="custom-select-search">
                            <i class="fas fa-search"></i>
                            <input type="text" class="custom-select-search-input" placeholder="搜索..." />
                        </div>
                    ` : ''}
                    <div class="custom-select-options">
                        ${this.items.map(item => this.renderOption(item)).join('')}
                    </div>
                </div>
            </div>
        `;

        this.displayEl = this.container.querySelector('.custom-select-display');
        this.dropdownEl = this.container.querySelector('.custom-select-dropdown');
        this.optionsEl = this.container.querySelector('.custom-select-options');
        this.arrowEl = this.container.querySelector('.custom-select-arrow');
        this.searchInputEl = this.container.querySelector('.custom-select-search-input');

        // 初始化时设置 data 属性
        if (this.options.multiple) {
            this.displayEl.dataset.selectedValues = JSON.stringify(this.selectedValues);
        } else {
            this.displayEl.dataset.value = this.selectedValues !== null ? String(this.selectedValues) : '';
        }
    }

    getDisplayText(selectedItems) {
        if (selectedItems.length === 0) {
            return this.options.placeholder;
        }
        
        if (this.options.multiple) {
            // 多选模式下，按"-"分割只展示简要部分（第一部分）
            return selectedItems.map(item => {
                const parts = item.label.split(' - ');
                return parts[0].trim();
            }).join(', ');
        }
        
        return selectedItems.map(item => item.label).join(', ');
    }

    renderOption(item) {
        const isSelected = this.options.multiple
            ? this.selectedValues.includes(item.value)
            : item.value === this.selectedValues;

        return `
            <div class="custom-select-option" data-value="${item.value}">
                ${this.options.multiple ? `
                    <span class="custom-select-checkbox ${isSelected ? 'checked' : ''}">
                        <i class="fas fa-check"></i>
                    </span>
                ` : ''}
                <span class="custom-select-option-label">${item.label}</span>
                ${!this.options.multiple && isSelected ? '<i class="fas fa-check custom-select-option-check"></i>' : ''}
            </div>
        `;
    }

    bindEvents() {
        this.boundHandlers.displayClick = (e) => {
            e.stopPropagation();
            this.toggle();
        };
        this.displayEl.addEventListener('click', this.boundHandlers.displayClick);

        this.boundHandlers.displayKeydown = (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggle();
            } else if (e.key === 'Escape') {
                this.close();
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.open();
                this.focusFirstOption();
            }
        };
        this.displayEl.addEventListener('keydown', this.boundHandlers.displayKeydown);

        this.boundHandlers.optionsClick = (e) => {
            const optionEl = e.target.closest('.custom-select-option');
            if (optionEl) {
                e.stopPropagation();
                this.selectOption(optionEl.dataset.value);
            }
        };
        this.optionsEl.addEventListener('click', this.boundHandlers.optionsClick);

        if (this.searchInputEl) {
            this.boundHandlers.searchInput = (e) => {
                const searchTerm = e.target.value.toLowerCase();
                const options = this.optionsEl.querySelectorAll('.custom-select-option');
                options.forEach(option => {
                    const label = option.querySelector('.custom-select-option-label').textContent.toLowerCase();
                    option.style.display = label.includes(searchTerm) ? 'flex' : 'none';
                });
            };
            this.searchInputEl.addEventListener('input', this.boundHandlers.searchInput);
        }

        this.boundHandlers.documentClick = (e) => {
            if (this.isOpen && !this.container.contains(e.target)) {
                this.close();
            }
        };
        document.addEventListener('click', this.boundHandlers.documentClick);

        this.boundHandlers.containerMouseEnter = () => {
            if (this.closeTimeout) {
                clearTimeout(this.closeTimeout);
                this.closeTimeout = null;
            }
        };
        this.container.addEventListener('mouseenter', this.boundHandlers.containerMouseEnter);

        this.boundHandlers.containerMouseLeave = () => {
            this.closeTimeout = setTimeout(() => {
                if (this.isOpen) {
                    this.close();
                }
            }, 50);
        };
        this.container.addEventListener('mouseleave', this.boundHandlers.containerMouseLeave);

        this.boundHandlers.dropdownMouseEnter = () => {
            if (this.closeTimeout) {
                clearTimeout(this.closeTimeout);
                this.closeTimeout = null;
            }
        };
        this.dropdownEl.addEventListener('mouseenter', this.boundHandlers.dropdownMouseEnter);

        this.boundHandlers.dropdownMouseLeave = () => {
            this.closeTimeout = setTimeout(() => {
                if (this.isOpen) {
                    this.close();
                }
            }, 50);
        };
        this.dropdownEl.addEventListener('mouseleave', this.boundHandlers.dropdownMouseLeave);
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.isOpen = true;
        this.dropdownEl.classList.add('show');
        this.displayEl.classList.add('focused');
        this.arrowEl.style.transform = 'rotate(180deg)';
    }

    close() {
        this.isOpen = false;
        this.dropdownEl.classList.remove('show');
        this.displayEl.classList.remove('focused');
        
        this.arrowEl.style.transform = 'rotate(0deg)';
        
        if (this.searchInputEl) {
            this.searchInputEl.value = '';
            const options = this.optionsEl.querySelectorAll('.custom-select-option');
            options.forEach(option => option.style.display = 'flex');
        }

        if (this.closeTimeout) {
            clearTimeout(this.closeTimeout);
            this.closeTimeout = null;
        }
    }

    selectOption(value) {
        if (this.options.multiple) {
            const index = this.selectedValues.indexOf(value);
            if (index > -1) {
                this.selectedValues.splice(index, 1);
            } else {
                this.selectedValues.push(value);
            }
        } else {
            this.selectedValues = value;
            this.close();
        }

        this.updateDisplay();
        this.renderOptions();
        
        if (this.options.onChange) {
            this.options.onChange(this.selectedValues, this);
        }
    }

    updateDisplay() {
        const selectedItems = this.items.filter(item =>
            this.options.multiple
                ? this.selectedValues.includes(item.value)
                : item.value === this.selectedValues
        );

        const displayText = this.getDisplayText(selectedItems);

        const displayTextEl = this.container.querySelector('.custom-select-display-text');
        if (displayTextEl) {
            displayTextEl.textContent = displayText;
        }

        // 同步更新 data 属性，确保 getValue() 能正确读取
        const display = this.container.querySelector('.custom-select-display');
        if (display) {
            if (this.options.multiple) {
                display.dataset.selectedValues = JSON.stringify(this.selectedValues);
            } else {
                display.dataset.value = this.selectedValues !== null ? String(this.selectedValues) : '';
            }
        }
    }

    renderOptions() {
        this.optionsEl.innerHTML = this.items.map(item => this.renderOption(item)).join('');
    }

    focusFirstOption() {
        const firstOption = this.optionsEl.querySelector('.custom-select-option');
        if (firstOption) {
            firstOption.focus();
        }
    }

    setItems(items) {
        this.items = items;
        this.updateDisplay();
        this.renderOptions();
    }

    setValue(value) {
        if (this.options.multiple) {
            this.selectedValues = Array.isArray(value) ? value : [value];
        } else {
            this.selectedValues = value;
        }
        this.updateDisplay();
        this.renderOptions();
    }

    getValue() {
        return this.selectedValues;
    }

    destroy() {
        this.close();

        if (this.displayEl && this.boundHandlers.displayClick) {
            this.displayEl.removeEventListener('click', this.boundHandlers.displayClick);
        }
        if (this.displayEl && this.boundHandlers.displayKeydown) {
            this.displayEl.removeEventListener('keydown', this.boundHandlers.displayKeydown);
        }
        if (this.optionsEl && this.boundHandlers.optionsClick) {
            this.optionsEl.removeEventListener('click', this.boundHandlers.optionsClick);
        }
        if (this.searchInputEl && this.boundHandlers.searchInput) {
            this.searchInputEl.removeEventListener('input', this.boundHandlers.searchInput);
        }
        if (this.boundHandlers.documentClick) {
            document.removeEventListener('click', this.boundHandlers.documentClick);
        }
        if (this.container && this.boundHandlers.containerMouseEnter) {
            this.container.removeEventListener('mouseenter', this.boundHandlers.containerMouseEnter);
        }
        if (this.container && this.boundHandlers.containerMouseLeave) {
            this.container.removeEventListener('mouseleave', this.boundHandlers.containerMouseLeave);
        }
        if (this.dropdownEl && this.boundHandlers.dropdownMouseEnter) {
            this.dropdownEl.removeEventListener('mouseenter', this.boundHandlers.dropdownMouseEnter);
        }
        if (this.dropdownEl && this.boundHandlers.dropdownMouseLeave) {
            this.dropdownEl.removeEventListener('mouseleave', this.boundHandlers.dropdownMouseLeave);
        }

        this.boundHandlers = {};
        this.container.innerHTML = '';
    }
}

// 全局工具函数：将页面中的原生 select 替换为自定义下拉组件
window.initCustomSelects = function() {
    const selects = document.querySelectorAll('select[data-custom-select]');
    selects.forEach(selectEl => {
        const container = selectEl.parentElement;
        const items = Array.from(selectEl.options).map(option => ({
            value: option.value,
            label: option.textContent
        }));

        const customSelect = new CustomSelect(container, {
            items: items,
            multiple: selectEl.multiple,
            placeholder: selectEl.dataset.placeholder || '请选择',
            searchable: selectEl.dataset.searchable === 'true',
            selectedValue: selectEl.value,
            onChange: (value) => {
                selectEl.value = value;
                selectEl.dispatchEvent(new Event('change'));
            }
        });

        selectEl.style.display = 'none';
    });
};

// 导出到全局
window.CustomSelect = CustomSelect;
