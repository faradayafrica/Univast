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
    validate(FormButton, textInput, errorEl, School, SchoorError, Faculty, FacultyError, FacultyCode, FacultyCodeError, Department, DepartmentError, DepartmentCode, DepartmentCodeError, DepartmentDegree, DepartmentDegreeError, DepartmentDuration, DepartmentDurationError, TwitterHandle);
  });
  
  const validate = async (buttonEl, inputField, errorField, School, SchoolError, Faculty, FacultyError, FacultyCode, FacultyCodeError, Department, DepartmentError, DepartmentCode, DepartmentCodeError, DepartmentDegree, DepartmentDegreeError, DepartmentDuration, DepartmentDurationError, TwitterHandle) => {

        const re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        if (School.value == '') {
            School.classList.add('error_active');
            SchoolError.innerHTML = 'Please select an institution';
            SchoolError.style.display = 'block';

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

            setTimeout(() => {
                DepartmentDuration.classList.remove('error_active');
                DepartmentDurationError.innerHTML = '';
                DepartmentDurationError.style.display = 'none';
            }, 2000);
        } else {

            try {
                buttonEl.innerHTML = '';
                buttonEl.style.display = 'flex';
                buttonEl.style.justifyContent = 'center';
                buttonEl.style.alignItems = 'center';
                const newSpan = document.createElement('div');
                buttonEl.disabled = true;
                newSpan.classList.add('loader');
                buttonEl.appendChild(newSpan);

                const airtableApiKey = 'pat3qhUQsq3ywg1nC.fb8f324b26db0d472b854724d54b74b5b42beff40d30b7e154531bf78ab9a95f';
                const tableId = 'appf0rZkii7KE9wfN';
                const tableName = 'tbl0KADfA7S7XUATC';
                const apiUrl = `https://api.airtable.com/v0/${airtableBaseId}/${tableId}`;
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

                if (response.status == 400) {
                    buttonEl.innerHTML = 'Request Access';
                    buttonEl.disabled = false;
                    inputField.classList.add('error_active');
                    errorField.innerHTML = 'Ouu, thank you but you are already on the waitlist.';
                    errorField.style.display = 'block';
                    setTimeout(() => {
                    inputField.classList.remove('error_active');
                    errorField.innerHTML = '';
                    errorField.style.display = 'none';
                    }, 3000);
                } else {
                    inputField.value = '';
                    buttonEl.disabled = true;
                    buttonEl.innerHTML = 'Welcome to Faraday!';
                    setTimeout(() => {
                    buttonEl.innerHTML = 'Request Access';
                    }, 4000);
                    buttonEl.disabled = false;
                }
            } catch (e) {
            buttonEl.innerHTML = 'Request Access';
            buttonEl.disabled = false;
            errorField.innerHTML = 'Something went wrong, please try again';
            }

        };
    }
