// Form Utilities - Unified JavaScript Module for BESshow
// Contains all form-related functionality including address handling, lunar date conversion,
// tooltips, search, and cart quantity controls

document.addEventListener('DOMContentLoaded', function() {
    console.log('BESshow Form Utilities initialized');

    // Initialize tooltips globally
    initializeTooltips();

    // Initialize address form functionality
    initializeAddressForm();

    // Initialize lunar date conversion
    initializeLunarForm();

    // Initialize search functionality
    initializeSearch();

    // Initialize cart quantity controls
    initializeCartQuantity();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    try {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    } catch (e) {
        console.error('Error initializing tooltips:', e);
    }
}

// Address form functionality
function initializeAddressForm() {
    try {
        const countySelect = document.getElementById('id_address_county');
        const districtSelect = document.getElementById('id_address_district');
        const zipCodeInput = document.getElementById('id_address_zip_code');

        if (countySelect && districtSelect) {
            const addressDataEl = countySelect;
            const addressData = addressDataEl.getAttribute('data-address-data');
            let addressJson = [];

            if (addressData) {
                addressJson = JSON.parse(addressData);
            }

            function updateDistrictOptions(selectedCounty) {
                districtSelect.innerHTML = '<option value="">請選擇鄉鎮市區</option>';
                if (selectedCounty && addressJson.length > 0) {
                    const cityData = addressJson.find(city => city.CityName === selectedCounty);
                    if (cityData && cityData.AreaList) {
                        cityData.AreaList.forEach(area => {
                            const option = document.createElement('option');
                            option.value = area.AreaName;
                            option.textContent = area.AreaName;
                            option.setAttribute('data-zipcode', area.ZipCode);
                            districtSelect.appendChild(option);
                        });
                    }
                }
            }

            function updateZipCode(selectedDistrict) {
                if (zipCodeInput && selectedDistrict) {
                    const selectedOption = districtSelect.querySelector(`option[value="${selectedDistrict}"]`);
                    if (selectedOption) {
                        const zipCode = selectedOption.getAttribute('data-zipcode');
                        if (zipCode) {
                            zipCodeInput.value = zipCode;
                        }
                    }
                }
            }

            const initialDistrict = districtSelect.value; // Store the initial value before it gets wiped

            if (countySelect.value) {
                updateDistrictOptions(countySelect.value); // This repopulates the district options
                if (initialDistrict) {
                    districtSelect.value = initialDistrict; // Re-apply the initial value
                    updateZipCode(districtSelect.value);   // Trigger zip code update
                }
            }

            countySelect.addEventListener('change', function() {
                updateDistrictOptions(this.value);
                if (zipCodeInput) {
                    zipCodeInput.value = '';
                }
            });

            districtSelect.addEventListener('change', function() {
                updateZipCode(this.value);
            });
        }
    } catch (e) {
        console.error('Error in address form functionality:', e);
    }
}

// Lunar date conversion functionality
function initializeLunarForm() {
    try {
        const gregorianDateInput = document.getElementById('id_gregorian_birth_date');
        const gregorianTimeInput = document.getElementById('id_gregorian_birth_time');
        const lunarDateInput = document.getElementById('id_lunar_birth_date');
        const lunarTimeInput = document.getElementById('id_lunar_birth_time');

        function updateLunarInfo() {
            if (gregorianDateInput && gregorianDateInput.value) {
                const selectedDate = new Date(gregorianDateInput.value);
                const selectedTime = gregorianTimeInput ? gregorianTimeInput.value : null;
                const lunarYear = selectedDate.getFullYear();
                const lunarMonth = selectedDate.getMonth() + 1;
                const lunarDay = selectedDate.getDate();

                if (lunarDateInput) {
                    lunarDateInput.value = `${lunarYear}-${lunarMonth}-${lunarDay}`;
                }

                if (lunarTimeInput && selectedTime) {
                    const timeParts = selectedTime.split(':');
                    const hour = parseInt(timeParts[0]);
                    const lunarHour = hour < 12 ? `上午${hour}時` : `下午${hour - 12}時`;
                    lunarTimeInput.value = lunarHour;
                } else if (lunarTimeInput) {
                    lunarTimeInput.value = '吉時';
                }
            }
        }

        if (gregorianDateInput) {
            gregorianDateInput.addEventListener('change', updateLunarInfo);
        }
        if (gregorianTimeInput) {
            gregorianTimeInput.addEventListener('change', updateLunarInfo);
        }
        if (gregorianDateInput && gregorianDateInput.value) {
            updateLunarInfo();
        }
    } catch (e) {
        console.error('Error in lunar date conversion:', e);
    }
}

// Search functionality for account list
function initializeSearch() {
    try {
        const searchInput = document.getElementById('userSearchInput');
        if (searchInput) {
            const accountRows = document.querySelectorAll('[data-account-row]');

            searchInput.addEventListener('input', function() {
                const filter = this.value.toLowerCase().trim();

                accountRows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(filter) || filter === '') {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        }
    } catch (e) {
        console.error('Error in search functionality:', e);
    }
}

// Cart quantity controls
function initializeCartQuantity() {
    try {
        // Make changeQuantity function globally available
        window.changeQuantity = function(button, delta) {
            const input = button.parentElement.querySelector('.quantity-input');
            let currentValue = parseInt(input.value) || 0;
            let newValue = currentValue + delta;

            if (newValue < 0) {
                newValue = 0;
            }

            input.value = newValue;
        };
    } catch (e) {
        console.error('Error in cart quantity functionality:', e);
    }
}