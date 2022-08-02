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
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
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
      const page = e.target.dataset.page;

      console.log(page);
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
                }

            const address = '/get_institution_api?'
            fetch(fetchAdress(address)).then(response => response.json()).then(data => {
                    if(isEmpty(data)) {
                      this.currentStep--
                    }
                    else {
                        this.updateForm();
                        show_id(address, crateChoiceHtml);
                        getCategoriesNames(ids)
                    }
                })
            }

            /* Step 2 */
            if (this.currentStep === 3) {
                if (checkBagsQuantity()) {
                    this.updateForm()
                    getBagsQuantity()
                } else {
                    this.currentStep--
                }
            }

            /* Step 3 */
            if (this.currentStep === 4) {
                const radio_id = getRadio()
                if(radio_id.length ===0 ) {
                  this.currentStep--
                }
                else {
                    this.updateForm()
                    getInstitutionName(radio_id)
                }
            }

            /* Step 4 */
            if (this.currentStep === 5) {
                const address = getAdress()
                const date = getDate()

                if (address && date) {
                    this.updateForm()
                    createAddressDateSummary(address, date)
                } else {
                    this.currentStep--
                }
            }

            /* Step 5 - form submit */
            if (this.currentStep === 6) {

                }

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
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
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
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  const table = document.querySelector('table#donations')
  table.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener("change", () => createUserDonations(checkbox)
      )
  })
});


//POBIERANIE API

function createUserDonations(checkbox) {
    fetch(`/get_donation_api/?id=${checkbox.value}`).then(response => response.json())
        .then(data => {
            const table = document.querySelector('table#donations')
            table.querySelectorAll('tr').forEach(tr => {tr.remove()});
            data.forEach(obj =>  {console.log(obj); createTr(data, obj)})
        })
}

function createTr(data, obj) {
    const tbody = document.querySelector('table#donations').firstElementChild
    const tr = document.createElement('tr')
    tr.setAttribute("style", "justify-content: left")
    tbody.appendChild(tr)

    const td1 = document.createElement('td')
    td1.innerText = obj.fields.institution
    if(obj.fields.is_taken) {
        td1.setAttribute("style", "font-size: 15px; color:gray")
    } else {
        td1.setAttribute("style", "font-size: 15px;")
    }
    tr.appendChild(td1)

    const td2 = document.createElement('td')
    td2.innerText = `${formatDate(obj)} ${formatTime(obj)}`
    if(obj.fields.is_taken) {
        td2.setAttribute("style", "font-size: 15px; color:gray")
    } else {
        td2.setAttribute("style", "font-size: 15px;")
    }
    tr.appendChild(td2)

    const td3 = document.createElement('td')
    td3.innerText = `${obj.fields.quantity} worków`
    if(obj.fields.is_taken) {
        td3.setAttribute("style", "font-size: 15px; color:gray")
    } else {
        td3.setAttribute("style", "font-size: 15px;")
    }
    tr.appendChild(td3)

    const td4 = document.createElement('td')
    td4.innerText = cateoriesToString(obj)
    if(obj.fields.is_taken) {
        td4.setAttribute("style", "font-size: 15px; color:gray")
    } else {
        td4.setAttribute("style", "font-size: 15px;")
    }
    tr.appendChild(td4)

    const td5 = document.createElement('td')
    const input = document.createElement('input')
    input.setAttribute("type", "checkbox")
    input.setAttribute("name", "iz_taken")
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


function show_id(address, func) {
    fetch(fetchAdress(address)).then(response => response.json())
        .then(data => data.forEach(obj => {
            func(obj)
        }))
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

function get_checked_chexboxes()
{
    const markedCheckbox = document.querySelectorAll('input[type="checkbox"]:checked');
    const ids = [];
    markedCheckbox.forEach(box => ids.push(box.value));
    return ids;
}


function crateChoiceHtml(institution) {

    const type_names = {
        1: 'Fundacja',
        2: 'Organizacja Pozarządowa',
        3: 'Lokalna Zbiórka'
    }

    let div = document.querySelector('#institutions');
    let button = document.querySelector('#form_button');

    const maindiv = document.createElement("div")
    maindiv.setAttribute("class", "form-group form-group--checkbox");
    maindiv.setAttribute('id', 'single-institution');
    div.insertBefore(maindiv, button)

    const label = document.createElement("label")
    maindiv.appendChild(label)

    const input = document.createElement("input")
    input.setAttribute("id", "institution_radio_checkbox")
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
  document.querySelectorAll('#single-institution').forEach(div => {div.remove()})
}

function isInt(value) {
  return !isNaN(value) &&
         parseInt(Number(value)) == value &&
         !isNaN(parseInt(value, 10));
}

function checkBagsQuantity() {
    const bags = document.querySelector('#bags_input').value
    return (isInt(bags) && bags > 0)
}

function getBagsQuantity() {
    const bags = document.querySelector('#bags_input').value
    const categoriesSummary = document.querySelector('#categories-summary')
    let bagsDeclination = 'worek'

    if (bags > 1 && bags < 5) {
        bagsDeclination = 'worki'
    } else if (bags >= 5) {
        bagsDeclination = 'worków'
    }

    categoriesSummary.innerHTML = `${bags} ${bagsDeclination} artykułów kategorii: ${categoriesSummary.innerHTML}`
}


function fetchAdress(address) {
    const ids = get_checked_chexboxes();
    const params = new URLSearchParams();
    ids.forEach(id => params.append("id", id))
    return  address + params.toString()
}

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
    const institutionSummary = document.querySelector('#institution_summary')
    institutionSummary.innerHTML = `${institutionName}`
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
    const categoriesSummary = document.querySelector('#categories-summary')
    categoriesSummary.innerHTML = categoriesNames.join(', ').toLowerCase()

}

function getAdress() {
    const adress = document.querySelector('[name="address"]').value
    console.log(adress)
    const city = document.querySelector('[name="city"]').value
        console.log(city)
    const postcode = document.querySelector('[name="zip_code"]').value
        console.log(postcode)
    const phone = document.querySelector('[name="phone_number"]').value
        console.log(phone)

    if (adress && city && postcode && phone) {
        return [adress, city, postcode, phone]
    } else {
        return false
    }

}

function getDate() {
    const date = document.querySelector('[name="pick_up_date"]').value
    const time = document.querySelector('[name="pick_up_time"]').value
    const moreInfo = document.querySelector('[name="pick_up_comment"]').value

    if (date && time && moreInfo) {
        return [date, time, moreInfo]
    } else {
        return false
    }
}

function createAddressDateSummary(address, date) {
    const div = document.querySelector('div[data-step="5"]')
    const addressList = div.querySelector('#address-list')
    const dateList = div.querySelector('#date-list')

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
    const addressList = div.querySelector('#address-list')
    const dateList = div.querySelector('#date-list')

    Array.from(addressList.children).forEach(li => li.remove())
    Array.from(dateList.children).forEach(li => li.remove())
}

// function createUserDonations(data) {
//     const table = document.querySelector('table#donations')
//     table.querySelectorAll('tr').forEach(tr => {tr.remove()});
//     data.forEach(obj =>  createTr(data, obj))
// }
//
// function createTr(data, obj) {
//         const tr = document.createElement('tr')
//         tr.setAttribute("style", "justify-content: left")
//         table.appendChild(tr)
//
//         const td1 = document.createElement('td')
//         td1.innerText=obj.fields.institution
//         tr.appendChild(td1)
//
//         const td2 = document.createElement('td')
//         td2.innerText=`${obj.fields.pick_up_date} ${obj.fields.pick_up_time}`
//         tr.appendChild(td2)
//
//         const td3 = document.createElement('td')
//         td3.innerText=obj.fields.quantity
//         tr.appendChild(td3)
//
//         const td4 = document.createElement('td')
//         td4.innerText=obj.fields.categories
//         tr.appendChild(td4)
//
//         const td5 = document.createElement('td')
//         const input = document.createElement('input')
//         input.setAttribute("type", "checkbox")
//         input.setAttribute("name", "is_taken")
//         input.setAttribute("value", obj.pk)
//         if(obj.fields.is_taken) {
//             input.setAttribute("checked", "checked")
//         }
//         input.addEventListener('change', () => createUserDonations(data))
//
//         td5.appendChild(input)
//         tr.appendChild(td5)
// }