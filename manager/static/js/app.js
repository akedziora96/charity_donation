document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
            this.changeSlide(e);
            createInstitutionsPage(getInstitutionType(), 1)
            setButtonActive(1)
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
            const targetPage = this.changePage(e);
            createInstitutionsPage(getInstitutionType(),targetPage)
            setButtonActive(targetPage)
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");

        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
        return e.target.dataset.page
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */



    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            this.currentStep++;

            /* Step 1 */
            if(this.currentStep === 2) {
                const ids = get_checked_chexboxes();
                if (ids.length === 0) {
                    this.currentStep--
                    DisplayMessage('Nie dokonano wyboru.')
                }
                else {
                    const address = '/get-institution-api?'
                    fetch(fetchAdress(address)).then(response => response.json()).then(data => {
                            if(isEmpty(data)) {
                                this.currentStep--
                                DisplayMessage('Brak organizacji jednocześnie przyjmującej dary wszystkich wybranych kategorii.')
                            }
                            else {
                                this.updateForm();
                                show_id(address, crateChoiceHtml);
                                getCategoriesNames(ids)
                                ClearMessages()
                    }
                })
                }
            }

            /* Step 2 */
            if (this.currentStep === 3) {
                if (checkBagsQuantity()) {
                    this.updateForm()
                    getBagsQuantity()
                    ClearMessages()
                } else {
                    this.currentStep--
                    DisplayMessage('Nieprawidłowa liczba worków.<br> Liczba worków musi być całkowita i dodatnia.')
                }
            }

            /* Step 3 */
            if (this.currentStep === 4) {
                const radio_id = getRadio()
                if(radio_id.length ===0 ) {
                    this.currentStep--
                    DisplayMessage('Nie dokonano wyboru.')

                }
                else {
                    this.updateForm()
                    getInstitutionName(radio_id)
                    ClearMessages()
                }
            }

            /* Step 4 */
            if (this.currentStep === 5) {
                const address = getAdress()

                if (address) {
                    const date = getDate()
                    if (date) {
                        this.updateForm()
                        createAddressDateSummary(address, date)
                        ClearMessages()
                    }
                    else {
                        this.currentStep--
                    }
                } else {
                    this.currentStep--
                    /*Displaymessage is called in getAdress and getFunction to get appropriate message text*/
                }
            }

            /* Step 5 - form submit */
            if (this.currentStep === 6) {}

        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
          if (this.currentStep === 1)
          {
            remove_all_institutions_html()
          }
          if (this.currentStep === 4) {
              removeAddressDateSummary()
          }
        });
      });

      // Form submit
      this.$form.querySelector('form').addEventListener("submit", e => this.submit(e));
      // TODO: in form.html, there is a onclick function to submit form. Move it here.
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }


    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
        const formData = new FormData(this.$form.querySelector('form'));
        const submitButton = document.querySelector('button#donation-form-submit');
        makeSubmitButtonWait(submitButton)


        fetch('/save-donation-api/', {
            method: 'post',
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.replace(data.url);
                } else if (data.status === 'error') {
                    setTimeout(function () {
                         DisplayMessage(data.error_message)
                         makeSubmitButtonDefault(submitButton)
                    },200)
                }
            })
            .catch(err => console.log(err))

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  const div = document.querySelector('div.user-donations')
    if (div) {
  div.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener("change", () => createUserDonations(checkbox)
      )
  })
    }

    const contactForm = document.querySelector('form.form--contact')
    contactForm.addEventListener("submit", e => submitConntact(e));


    function submitConntact(e) {
        console.log(this)
        e.preventDefault();
        const contactSubmitButton = document.querySelector('button#contact-form-submit')
        makeSubmitButtonWait(contactSubmitButton)

        const contactForm = document.querySelector('form.form--contact')
        const contactFormData = new FormData(contactForm);

        fetch('/contact-us-api/', {
            method: 'post',
            body: contactFormData
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.replace(data.url);
                } else if (data.status === 'error') {
                    setTimeout(function () {
                        displayErrors(data)
                        makeSubmitButtonDefault(contactSubmitButton)
                    },200)
                }
            })
            .catch(err => console.log(err))
    }

});






//EXTENDED FUNCTIONS

//DYNAMIC INSTITUTIONS PAGINATED DISPLAY ON LANDING PAGE

function getInstitutionType() {
    return document.querySelector('ul.help--buttons')
        .querySelector('a.active').parentElement.dataset.id

}

function getCurrentPage() {
    return document.querySelector('ul.help--slides-pagination')
        .querySelector('a.active').dataset.page
}

function setButtonActive(targetPage) {
    const currentButton = document.querySelector('ul.help--slides-pagination')
        .querySelector(`a[data-page="${getCurrentPage()}"]`)
    currentButton.classList.remove('active')

    const nextButton = document.querySelector('ul.help--slides-pagination')
        .querySelector(`a[data-page="${targetPage}"]`)
    nextButton.classList.add('active')
}

function createInstitutionsPage(institutionType, pageNum) {
    fetch(`/get-page-api/?type=${institutionType}&page=${pageNum}`).then(response => response.json())
        .then(data => {createInstitutionsPageHtml(institutionType, data)})

}

function createInstitutionsPageHtml(institutionType, data) {
    const list = document.querySelector("section#help").
    querySelector(`div[data-id="${institutionType}"]`).
    querySelector('ul')

    list.querySelectorAll('li').forEach(li => li.remove())

    data.forEach(obj => {
        const li = document.createElement('li')
        list.appendChild(li)

        const div = document.createElement('div')
        div.setAttribute('class', 'col')
        li.appendChild(div)

        const div2 = document.createElement('div')
        div2.setAttribute('class', 'title')
        div2.innerHTML = `"${obj.fields.name}"`
        div.appendChild(div2)

        const div3 = document.createElement('div')
        div3.setAttribute('class', 'subtitle')
        div3.innerHTML = obj.fields.description
        div.appendChild(div3)

        const div4 = document.createElement('div')
        div4.setAttribute('class', 'col')
        li.appendChild(div4)

        const div5 = document.createElement('div')
        div5.setAttribute('class', 'text')
        div5.innerHTML = obj.fields.categories
        div4.appendChild(div5)

    })
    console.log(list)
}





//DYNAMIC DONATION  DISPLAY ON USER PROFILE PAGE

function createUserDonations(checkbox) {
    fetch(`/get-donation-api/?id=${checkbox.value}`).then(response => response.json())
        .then(data => {
            const div = document.querySelector('div.user-donations')
            div.querySelectorAll('tr').forEach(tr => {tr.remove()});
            data.forEach(obj =>  {console.log(obj); createTr(data, obj)})
        })
}

function createTr(data, obj) {
    const tbody = document.querySelector('div.user-donations').querySelector('tbody')
    const tr = document.createElement('tr')
    if(obj.fields.is_taken) {
        tr.setAttribute("class", "taken")
    } else {
        tr.setAttribute("class", "untaken")
    }
    tbody.appendChild(tr)

    const td1 = document.createElement('td')
    td1.innerText = obj.fields.institution
    tr.appendChild(td1)

    const td2 = document.createElement('td')
    td2.innerText = `${formatDate(obj)} ${formatTime(obj)}`
    tr.appendChild(td2)

    const td3 = document.createElement('td')
    td3.innerText = `${obj.fields.quantity} worków`
    tr.appendChild(td3)

    const td4 = document.createElement('td')
    td4.innerText = cateoriesToString(obj)
    tr.appendChild(td4)

    const td5 = document.createElement('td')
    const input = document.createElement('input')
    input.setAttribute("type", "checkbox")
    input.setAttribute("name", "is_taken")
    input.setAttribute("value", obj.pk)

    input.checked = !!obj.fields.is_taken;

    input.addEventListener('change', () => createUserDonations(input))

    td5.appendChild(input)
    tr.appendChild(td5)

}

function cateoriesToString(obj) {
    return (obj.fields.categories).join(', ')
}

function formatDate(obj) {
    const months = {
        '01': 'stycznia',
        '02': 'lutego',
        '03': 'marca',
        '04': 'kwietnia',
        '05': 'maja',
        '06': 'czerwca',
        '07': 'lipca',
        '08': 'sierpnia',
        '09': 'września',
        '10': 'października',
        '11': 'listopada',
        '12': 'grudnia',

    }
    const originalDate = obj.fields.pick_up_date.split('-')
    return `${parseInt(originalDate[2], 10)} ${months[originalDate[1]]} ${originalDate[0]}`
}

function formatTime(obj) {
    const originalTime = obj.fields.pick_up_time.split(':')
    return `${originalTime[0]}:${originalTime[1]}`
}




//DYNAMIC DONATION-ADD FORM DISPLAY AND VALIDATION OF FORM FIELDS

//STEP ONE
function fetchAdress(address) {
    const ids = get_checked_chexboxes();
    const params = new URLSearchParams();
    ids.forEach(id => params.append("id", id))
    return  address + params.toString()
}

function get_checked_chexboxes()
{
    const markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
    const ids = [];
    markedCheckbox.forEach(box => ids.push(box.value));
    return ids;
}

function show_id(address, func) {
    fetch(fetchAdress(address)).then(response => response.json())
        .then(data => data.forEach(obj => {
            func(obj)
        }))
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}


function crateChoiceHtml(institution) {

    const type_names = {
        1: 'Fundacja',
        2: 'Organizacja Pozarządowa',
        3: 'Lokalna Zbiórka'
    }

    let div = document.querySelector('div#institutions');
    let button = div.querySelector('div.form-group--buttons');

    const maindiv = document.createElement("div")
    maindiv.setAttribute("class", "form-group form-group--checkbox");
    // maindiv.setAttribute('id', 'single-institution');
    div.insertBefore(maindiv, button)

    const label = document.createElement("label")
    maindiv.appendChild(label)

    const input = document.createElement("input")
    input.setAttribute("type", "radio")
    input.setAttribute("name", "institution")
    input.setAttribute("value", institution.pk)
    label.appendChild(input)

    const span1 = document.createElement("span")
    span1.setAttribute("class", "checkbox radio")
    label.appendChild(span1)

    const span2 = document.createElement("span")
    span2.setAttribute("class", "description")
    label.appendChild(span2)

    const div1 = document.createElement("div")
    div1.setAttribute("class", "title")
    div1.innerHTML = `${type_names[institution.fields.type]} "${institution.fields.name}"`
    span2.appendChild(div1)

    const div2 = document.createElement("div")
    div2.setAttribute("class", "subtitle")
    div2.innerHTML = `Cel i misja: ${institution.fields.description}`
    span2.appendChild(div2)
}

function remove_all_institutions_html () {
    let div = document.querySelector('div#institutions');
    div.querySelectorAll('div.form-group--checkbox').forEach(div => {div.remove()})
}

function isInt(value) {
  return !isNaN(value) &&
         parseInt(Number(value)) == value &&
         !isNaN(parseInt(value, 10));
}

function getCategoriesNames(ids) {
    const div = document.querySelector('div[data-step="1"]')
    const checked_categories = []
    ids.forEach(id => {
        checked_categories.push(div.querySelector(`input[value="${id}"]`))
    })
    const categoriesNames = []
    checked_categories.forEach(input => {
        categoriesNames.push(input.nextElementSibling.nextElementSibling.innerHTML)
    })
    const spanCategories = document.querySelector('span#categories')
    spanCategories.innerHTML = categoriesNames.join(', ').toLowerCase()

}


//STEP TWO
function checkBagsQuantity() {
    const bags = document.querySelector('input#bags').value
    return (isInt(bags) && bags > 0)
}

function getBagsQuantity() {
    const bags = document.querySelector('input#bags').value
    const spanBags = document.querySelector('span#bags')
    let bagsDeclination = 'worek'

    if (bags > 1 && bags < 5) {
        bagsDeclination = 'worki'
    } else if (bags >= 5) {
        bagsDeclination = 'worków'
    }

    spanBags.innerHTML = `${bags} ${bagsDeclination} artykułów kategorii: `
}


//STEP THREE
function getRadio() {
    let markedCheckbox = document.querySelectorAll('input[type="radio"]:checked');
    let radio_id = [];
    markedCheckbox.forEach(box => radio_id.push(box.value));
    return radio_id
}

function getInstitutionName(id) {
    const div = document.querySelector('div#institutions')
    const input = div.querySelector(`input[value="${id}"]`)
    const institutionName = input.nextSibling.nextSibling.firstChild.innerHTML
    const institutionSummary = document.querySelector('span#institution-summary')
    institutionSummary.innerHTML = `${institutionName}`
}


//STEP FOUR
function getAdress() {
    const address = document.querySelector('input[name="address"]').value
    const addressRegex = new RegExp(
        /^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+([-|\s]?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)*\s\d{0,5}\/?\d{0,5}[a-zA-Z]?)$/
    );
    if (! addressRegex.test(address)) {
        DisplayMessage('Nieprawidłowy adres.')
        return false
    }

    let city = document.querySelector('input[name="city"]').value
    const cityNameRegex = new RegExp(
        /^(([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])+([-|\s]?([A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ])*)*)$/
    );
    if (! cityNameRegex.test(city)) {
        DisplayMessage('Nieprawidłowa nazwa miasta.')
        return false
    }

    let postcode = document.querySelector('input[name="zip_code"]').value
    const postcodeRegex = new RegExp(
        /^((\d{2}-\d{3})|\d{5})$/
    );
    if (! postcodeRegex.test(postcode)) {
        DisplayMessage('Nieprawidłowy kod pocztowy')
        return false
    }

    let phone = document.querySelector('input[name="phone_number"]').value
    const phoneRegex = new RegExp(
        /(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)/
    );
    if (! phoneRegex.test(phone)) {
        DisplayMessage('Nieprawidłowy numer telefony')
        return false
    }

    return [address, city, postcode, phone]
}

function getDate() {
    let date = document.querySelector('input[name="pick_up_date"]').value
    const dateToday = new Date();
    const dateInput = new Date(date);
    if ((dateInput.getDate() < dateToday.getDate()) || !date) {
        DisplayMessage('Nieprawidłowa data odbioru<br>lub data odbioru jest z przeszłości.')
        return false
    }

    let time = document.querySelector('input[name="pick_up_time"]').value
    const splitedTime = time.split(":");
    const hour = splitedTime[0]
    const minutes = splitedTime[1]
    const timeNow = new Date();
    const timeInput = new Date();
    timeInput.setHours(hour, minutes, 0, 0)
    if (dateInput.getDate() <= dateToday.getDate() && timeInput.getTime() < timeNow.getTime() || !time) {
        DisplayMessage('Nieprawidłowa godzina odbioru<br>lub godzina odbioru jest z przeszłości.')
        return false
    }

    let moreInfo = document.querySelector('textarea[name="pick_up_comment"]').value
    moreInfo = moreInfo.trim()
    if  (moreInfo.length == 0) {
        DisplayMessage('Nieprawidłowy komentarz.')
        return false
    }

    return [date, time, moreInfo]

}

function createAddressDateSummary(address, date) {
    const div = document.querySelector('div[data-step="5"]')
    const addressList = div.querySelector('ul#address-list')
    const dateList = div.querySelector('ul#date-list')

    address.forEach(item => {
        let li = document.createElement('li')
        li.innerHTML = item
        addressList.appendChild(li)
    })

    date.forEach(item => {
        let li = document.createElement('li')
        li.innerHTML = item
        dateList.appendChild(li)
    })
}


function removeAddressDateSummary() {
    const div = document.querySelector('div[data-step="5"]')
    const addressList = div.querySelector('ul#address-list')
    const dateList = div.querySelector('ul#date-list')

    Array.from(addressList.children).forEach(li => li.remove())
    Array.from(dateList.children).forEach(li => li.remove())
}


function DisplayMessage(text) {
    const parentDiv = document.querySelector('div.active').querySelector('.form-group--buttons')
    const messageDiv = parentDiv.querySelector('div.message')

    if (messageDiv) {
        messageDiv.remove()
    }

    const newMessageDiv = document.createElement('div')
    newMessageDiv.setAttribute('class', 'message')
    parentDiv.appendChild(newMessageDiv)

    const textDiv = document.createElement('div')
    textDiv.setAttribute('class', 'message-text')
    newMessageDiv.appendChild(textDiv)
    textDiv.innerHTML = text

    const closeDiv = document.createElement('div')
    closeDiv.setAttribute('class', 'message-close')
    closeDiv.innerHTML = "&#215"
    newMessageDiv.appendChild(closeDiv)

    closeDiv.addEventListener('click', () => newMessageDiv.remove())
}

function ClearMessages() {
    const parentDivs = document.querySelectorAll('.form-group--buttons')

    parentDivs.forEach(parentDiv => {
        Array.from(parentDiv.querySelectorAll('div.message')).forEach(messageDiv => messageDiv.remove())
        }
    )

}

function makeSubmitButtonWait(button) {
    button.innerHTML = 'Oczekiwanie'
    document.body.style.cursor = 'wait';
    document.querySelectorAll('button').forEach(button => button.style.cursor='wait')

    document.querySelectorAll('button')
        .forEach(button => button.setAttribute('disabled', 'disabled'))
    document.querySelectorAll('a')
    .forEach(a => a.setAttribute('disabled', 'disabled'))
}

function makeSubmitButtonDefault(button) {
    button.innerHTML = 'Potwierdzam'
    document.body.style.cursor = 'default'
    document.querySelectorAll('button').forEach(button => button.style.cursor='pointer')

    document.querySelectorAll('button')
    .forEach(button => button.removeAttribute('disabled'))
    document.querySelectorAll('a')
    .forEach(a => a.removeAttribute('disabled'))
}

function displayErrors(data) {
    const keys = Object.keys(data.fields_errors)
        keys.forEach(singleKey => {
        const invalidElement = document.querySelector('form.form--contact').querySelector(`input[name="${singleKey}"]`)
        invalidElement.value = ''
        invalidElement.placeholder = data.fields_errors[singleKey]
        invalidElement.style.setProperty("--c", "red")
        invalidElement.style.setProperty("--o", "1")
        invalidElement.style.setProperty("--w", "bold")
    })
}