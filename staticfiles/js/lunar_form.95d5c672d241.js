document.addEventListener('DOMContentLoaded', function() {
    try {
        // Lunar date conversion functionality
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
        console.error('An error occurred in the lunar date conversion script:', e);
    }
});