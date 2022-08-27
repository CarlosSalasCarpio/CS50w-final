document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#button_admin_csv').addEventListener('click', () => admin_csv());
    document.querySelector('#button_admin_pdf').addEventListener('click', () => admin_pdf());
    document.querySelector('#back_to_admin_main').addEventListener('click', () => admin_main());
  
    // By default, load the inbox
    admin_main();
  
});

function admin_csv() {

    document.querySelector('#admin_csv_view').style.display = 'block';
    document.querySelector('#admin_pdf_view').style.display = 'none';
    document.querySelector('#admin_pdf_table').style.display = 'none';
    document.querySelector('#admin_main_view').style.display = 'none';
    document.querySelector('#back_to_admin_main').style.display = 'block';

}

function admin_pdf() {

    document.querySelector('#admin_csv_view').style.display = 'none';
    document.querySelector('#admin_pdf_view').style.display = 'block';
    document.querySelector('#admin_pdf_table').style.display = 'block';
    document.querySelector('#admin_main_view').style.display = 'none';
    document.querySelector('#back_to_admin_main').style.display = 'block';

}

function admin_main() {

    document.querySelector('#admin_csv_view').style.display = 'none';
    document.querySelector('#admin_pdf_view').style.display = 'none';
    document.querySelector('#admin_pdf_table').style.display = 'none';
    document.querySelector('#admin_main_view').style.display = 'block';
    document.querySelector('#back_to_admin_main').style.display = 'none';

}