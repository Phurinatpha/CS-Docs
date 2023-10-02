// Add a click event listener to all "delete" buttons with the class "btn-del"
function delete_button_sweet(ref_num, ref_year) {
  console.log("delete")
  Swal.fire({
    titleText: 'ยืนยันการลบข้อมูล ?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'ลบข้อมูล',
    cancelButtonText: 'ยกเลิก',


  }).then((result) => {
    if (result.isConfirmed) {

      delete_doc(ref_num, ref_year)
      Swal.fire({
        title: 'ลบเอกสารคำสั่งสำเร็จ !',
        icon: 'success',
        confirmButtonColor: '#3EBC2A',
        confirmButtonText: 'ตกลง', // Change the text of the confirmation button
        html: 'ปิดอัตโนมัติใน <b></b> วินาที', // Change the text to indicate seconds
        timer: 5000, // Change the timer to 5 seconds
        timerProgressBar: true,
        didOpen: () => {
          const b = Swal.getHtmlContainer().querySelector('b')
          timerInterval = setInterval(() => {
            b.textContent = Math.round(Swal.getTimerLeft() / 1000);
          }, 100); // Update the timer every second
        },
      });
    }
  });
}


function user_delete_sweet(id) {
  console.log("delete")
  Swal.fire({
    titleText: 'ยืนยันการลบข้อมูล ?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'ลบข้อมูล',
    cancelButtonText: 'ยกเลิก',


  }).then((result) => {
    if (result.isConfirmed) {

      delete_user(id)
      Swal.fire({
        title: 'ลบสิทธิ์สำเร็จ !',
        icon: 'success',
        confirmButtonColor: '#3EBC2A',
        confirmButtonText: 'ตกลง', // Change the text of the confirmation button
        html: 'ปิดอัตโนมัติใน <b></b> วินาที', // Change the text to indicate seconds
        timer: 5000, // Change the timer to 5 seconds
        timerProgressBar: true,
        didOpen: () => {
          const b = Swal.getHtmlContainer().querySelector('b')
          timerInterval = setInterval(() => {
            b.textContent = Math.round(Swal.getTimerLeft() / 1000);
          }, 100); // Update the timer every second
        },
      });
    }
  });
}

function user_logout() {
  console.log("logout")
  Swal.fire({
    titleText: 'กรุณาเข้าสู่ระบบใหม่อีกครั้ง',
    icon: 'warning',
    showCancelButton: false,
    confirmButtonColor: '#3085d6',
    confirmButtonText: 'ตกลง',


  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = '/logout';
    }
    else{
      window.location.href = '/logout';
    }
  });
}
