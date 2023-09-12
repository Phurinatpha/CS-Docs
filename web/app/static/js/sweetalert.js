
// Add a click event listener to all "delete" buttons with the class "btn-del"
function delete_button_sweet(id)  {
  console.log("delete")
    Swal.fire({
      titleText: 'ยืนยันการลบข้อมูล ?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#BABABA',
      confirmButtonText: 'ลบข้อมูล',
      cancelButtonText: 'ยกเลิก',


    }).then((result) => {
      if (result.isConfirmed) {
        
        delete_doc(id)
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

