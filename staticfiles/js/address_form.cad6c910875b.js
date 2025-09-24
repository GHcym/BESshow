document.addEventListener('DOMContentLoaded', function() {
    try {
        // Address selection functionality
        const countySelect = document.getElementById('id_address_county');
        const districtSelect = document.getElementById('id_address_district');
        const zipCodeInput = document.getElementById('id_address_zip_code');

        if (countySelect && districtSelect) {
            const addressData = countySelect.getAttribute('data-address-data');
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

            if (countySelect.value) {
                updateDistrictOptions(countySelect.value);
                const currentDistrict = districtSelect.getAttribute('value') || districtSelect.value;
                if (currentDistrict) {
                    setTimeout(() => {
                        districtSelect.value = currentDistrict;
                    }, 10);
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
        console.error('An error occurred in the address selection script:', e);
    }
});