var thaiDatePicker = new Palitday(
  {
    field: document.getElementById('thaiDatePicker'),
    // nuchYearFormat: ["BE","AD"], this will display year as 2566 (2023)
    nuchYearFormat: ["BE"],
    format: 'DD/MM/YYYY',
    i18n: {
      previousMonth: 'เดือนก่อนหน้า',
      nextMonth: 'เดือนถัดไป',
      months: ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'],
      weekdays: ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'],
      weekdaysShort: ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'],
    },
    onSelect: function () {
      const selectedDate = thaiDatePicker.getDate();
      const selectedYear = selectedDate.getFullYear();
      const thaiBuddhistYear = selectedYear + 543;
      const inputField = document.getElementById('thaiDatePicker');
      inputField.value = inputField.value.replace(/\d{4}\s*/, thaiBuddhistYear); // Replace the year part of the input value
    }
  });

  