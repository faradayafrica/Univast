$(function () {
    // ------------------------------------------------------- //
    // Scroll Top Button
    // ------------------------------------------------------- //
    $('#scrollTop').on('click', function () {
      $('html, body').animate({ scrollTop: 0 }, 1500);
    });
  
    var c,
      currentScrollTop = 0,
      navbar = $('.navbar');
    $(window).on('scroll', function () {
      // Navbar functionality
      var a = $(window).scrollTop(),
        b = navbar.height();
  
      currentScrollTop = a;
      if (c < currentScrollTop && a > b + b) {
        navbar.addClass('scrollUp');
      } else if (c > currentScrollTop && !(a <= b)) {
        navbar.removeClass('scrollUp');
      }
      c = currentScrollTop;
  
      if ($(window).scrollTop() >= 500) {
        $('#scrollTop').addClass('active');
      } else {
        $('#scrollTop').removeClass('active');
      }
    });
  
    // ---------------------------------------------------------- //
    // Preventing URL update on navigation link click
    // ---------------------------------------------------------- //
    $('.link-scroll').on('click', function (e) {
      var anchor = $(this);
      $('html, body')
        .stop()
        .animate(
          {
            scrollTop: $(anchor.attr('href')).offset().top,
          },
          1000
        );
      e.preventDefault();
    });
  
    // ---------------------------------------------------------- //
    // Scroll Spy
    // ---------------------------------------------------------- //
    $('body').scrollspy({
      target: '#navbarSupportedContent',
      offset: 80,
    });
  
    // ------------------------------------------------------- //
    // Navbar Toggler Button
    // ------------------------------------------------------- //
    $('.navbar .navbar-toggler').on('click', function () {
      $(this).toggleClass('active');
    });
  });
  
  const FormButton = document.querySelector('.newsletterForm button');
  
  FormButton.addEventListener('click', e => {
    e.preventDefault();
    const textInput = document.querySelector('.newsletterForm input');
    const errorEl = document.querySelector('.error_isActiveText');
    const success = document.querySelector('.success_isActiveText');

    const School = document.querySelector('#institution');
    const SchoorError = document.querySelector('.institution_error_isActiveText');

    const Faculty = document.querySelector('#schoolfaculty');
    const FacultyError = document.querySelector('.schoolfaculty_error_isActiveText');

    const FacultyCode = document.querySelector('#schoolfacultycode');
    const FacultyCodeError = document.querySelector('.schoolfacultycode_error_isActiveText');

    const Department = document.querySelector('#department');
    const DepartmentError = document.querySelector('.department_error_isActiveText');

    const DepartmentCode = document.querySelector('#departmentcode');
    const DepartmentCodeError = document.querySelector('.departmentcode_error_isActiveText');

    const DepartmentDegree = document.querySelector('#departmentdegree');
    const DepartmentDegreeError = document.querySelector('.departmentdegree_error_isActiveText');

    const DepartmentDuration = document.querySelector('#departmentduration');
    const DepartmentDurationError = document.querySelector('.departmentduration_error_isActiveText');

    const TwitterHandle = document.querySelector('#twitterhandle');
    validate(FormButton, textInput, errorEl, success, School, SchoorError, Faculty, FacultyError, FacultyCode, FacultyCodeError, Department, DepartmentError, DepartmentCode, DepartmentCodeError, DepartmentDegree, DepartmentDegreeError, DepartmentDuration, DepartmentDurationError, TwitterHandle);
  });

  const validate = async (buttonEl, inputField, errorField, successField, School, SchoolError, Faculty, FacultyError, FacultyCode, FacultyCodeError, Department, DepartmentError, DepartmentCode, DepartmentCodeError, DepartmentDegree, DepartmentDegreeError, DepartmentDuration, DepartmentDurationError, TwitterHandle) => {

    function validateForm() {
        let isValid = true;
      
        if (School.value == '') {
          School.classList.add('error_active');
          SchoolError.innerHTML = 'Please select an institution';
          SchoolError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            School.classList.remove('error_active');
            SchoolError.innerHTML = '';
            SchoolError.style.display = 'none';
          }, 2000);
        }
      
        if (Faculty.value.length == 0) {
          Faculty.classList.add('error_active');
          FacultyError.innerHTML = 'Please provide a value';
          FacultyError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            Faculty.classList.remove('error_active');
            FacultyError.innerHTML = '';
            FacultyError.style.display = 'none';
          }, 2000);
        }
      
        if (FacultyCode.value.length == 0) {
          FacultyCode.classList.add('error_active');
          FacultyCodeError.innerHTML = 'Please provide a value';
          FacultyCodeError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            FacultyCode.classList.remove('error_active');
            FacultyCodeError.innerHTML = '';
            FacultyCodeError.style.display = 'none';
          }, 2000);
        }
      
        if (Department.value.length == 0) {
          Department.classList.add('error_active');
          DepartmentError.innerHTML = 'Please provide a value';
          DepartmentError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            Department.classList.remove('error_active');
            DepartmentError.innerHTML = '';
            DepartmentError.style.display = 'none';
          }, 2000);
        }
      
        if (DepartmentCode.value.length == 0) {
          DepartmentCode.classList.add('error_active');
          DepartmentCodeError.innerHTML = 'Please provide a value';
          DepartmentCodeError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            DepartmentCode.classList.remove('error_active');
            DepartmentCodeError.innerHTML = '';
            DepartmentCodeError.style.display = 'none';
          }, 2000);
        }
      
        if (DepartmentDegree.value.length == 0) {
          DepartmentDegree.classList.add('error_active');
          DepartmentDegreeError.innerHTML = 'Please provide a value';
          DepartmentDegreeError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            DepartmentDegree.classList.remove('error_active');
            DepartmentDegreeError.innerHTML = '';
            DepartmentDegreeError.style.display = 'none';
          }, 2000);
        }
      
        if (DepartmentDuration.value.length == 0) {
          DepartmentDuration.classList.add('error_active');
          DepartmentDurationError.innerHTML = 'Please provide a value';
          DepartmentDurationError.style.display = 'block';
          isValid = false;
      
          setTimeout(() => {
            DepartmentDuration.classList.remove('error_active');
            DepartmentDurationError.innerHTML = '';
            DepartmentDurationError.style.display = 'none';
          }, 2000);
        }
      
        return isValid;
      }

    if (validateForm()) {

        buttonEl.innerHTML = '';
        buttonEl.style.display = 'flex';
        buttonEl.style.justifyContent = 'center';
        buttonEl.style.alignItems = 'center';
        const newSpan = document.createElement('div');
        buttonEl.disabled = true;
        newSpan.classList.add('loader');
        buttonEl.appendChild(newSpan);

        const apiUrl = `https://api.airtable.com/v0/${airtableBaseId}/${airtabletableId}`;
        const headers = {
        Authorization: `Bearer ${airtableApiKey}`,
        'Content-Type': 'application/json'
        };

        const data = {
            'School': School.value,
            'Faculty': Faculty.value,
            'FacultyCode': FacultyCode.value,
            'Department': Department.value,
            'DepartmentCode': DepartmentCode.value,
            'DepartmentDegree': DepartmentDegree.value,
            'DepartmentDuration': DepartmentDuration.value,
            'TwitterHandle': TwitterHandle.value,
        };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ fields: data }),
            }
        );

        if (response.status != 200) {
            buttonEl.innerHTML = 'Try Again';
            buttonEl.disabled = false;

            errorField.innerHTML = 'Sorry, something went wrong. Please try again.';
            errorField.style.display = 'block';

            setTimeout(() => {

                errorField.innerHTML = '';
                errorField.style.display = 'none';

            }, 3000);

        } else {
            
            School.value = '';
            Faculty.value = '';
            FacultyCode.value = '';
            Department.value = '';
            DepartmentCode.value = '';
            DepartmentDegree.value = '';
            DepartmentDuration.value = '';
            TwitterHandle.value = '';

            buttonEl.disabled = true;
            buttonEl.innerHTML = 'Submit another';
            successField.innerHTML = 'Thank you for providing this information, we greatly appreciate it.';
            successField.style.display = 'block';

            setTimeout(() => {

                successField.innerHTML = '';
                successField.style.display = 'none';
                buttonEl.disabled = false;

            }, 4000);

        }

    } else {
        // form is not valid, display an error message or do nothing
      }

    
    }
