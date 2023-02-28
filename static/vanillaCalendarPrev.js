let vanillaCalendarPrev = {
  month: document.querySelectorAll('[data-calendar-area="month-prev"]')[0],
  next: document.querySelectorAll('[data-calendar-toggle="next-prev"]')[0],
  previous: document.querySelectorAll(
    '[data-calendar-toggle="previous-prev"]'
  )[0],
  label: document.querySelectorAll('[data-calendar-label="month-prev"]')[0],
  activeDates: null,
  date: new Date(),
  prevDate: new Date(),
  todaysDate: new Date(),

  init: function (options) {
    this.options = options;
    this.date.setDate(1);
    this.createMonth();
    this.createListeners();
    this.previous.click();
  },

  createListeners: function () {
    let _this = this;
    this.next.addEventListener("click", function () {
      _this.clearCalendar();
      let nextMonth = _this.date.getMonth() + 1;
      _this.date.setMonth(nextMonth);
      _this.createMonth();
    });
    // Clears the calendar and shows the previous month
    this.previous.addEventListener("click", function () {
      _this.clearCalendar();
      let prevMonth = _this.date.getMonth() - 1;
      _this.date.setMonth(prevMonth);
      _this.createMonth();
    });
  },

  createDay: function (num, day, year) {
    let newDay = document.createElement("div");
    let dateEl = document.createElement("span");
    dateEl.innerHTML = num;
    newDay.className = "vcal-date";
    newDay.setAttribute("data-calendar-date", this.date);

    // if it's the first day of the month
    if (num === 1) {
      if (day === 0) {
        newDay.style.marginLeft = 6 * 14.28 + "%";
      } else {
        newDay.style.marginLeft = (day - 1) * 14.28 + "%";
      }
    }

    if (true && this.date.getTime() <= this.todaysDate.getTime() - 1) {
      newDay.classList.add("vcal-date--disabled");
    } else {
      newDay.classList.add("vcal-date--active");
      newDay.setAttribute("data-calendar-status", "active-prev");
    }

    if (this.date.toString() === this.todaysDate.toString()) {
      newDay.classList.add("vcal-date--today");
    }

    newDay.appendChild(dateEl);
    this.month.appendChild(newDay);
  },

  dateClicked: function () {
    let _this = this;
    this.activeDates = document.querySelectorAll(
      '[data-calendar-status="active-prev"]'
    );
    for (let i = 0; i < this.activeDates.length; i++) {
      this.activeDates[i].addEventListener("click", function (event) {
        let picked = document.querySelectorAll(
          '[data-calendar-label="picked"]'
        )[0];
        picked.innerHTML = this.dataset.calendarDate;
        _this.removeActiveClass();
        this.classList.add("vcal-date--selected");
      });
    }
  },

  createMonth: function () {
    let currentMonth = this.date.getMonth();
    while (this.date.getMonth() === currentMonth) {
      this.createDay(
        this.date.getDate(),
        this.date.getDay(),
        this.date.getFullYear()
      );
      this.date.setDate(this.date.getDate() + 1);
    }
    // while loop trips over and day is at 30/31, bring it back
    this.date.setDate(1);
    this.date.setMonth(this.date.getMonth() - 1);

    this.label.innerHTML =
      this.monthsAsString(this.date.getMonth()) + " " + this.date.getFullYear();
    this.dateClicked();
  },

  monthsAsString: function (monthIndex) {
    return [
      "Январь",
      "Февраль",
      "Март",
      "Апрель",
      "Май",
      "Июнь",
      "Июль",
      "Август",
      "Сентябрь",
      "Октябрь",
      "Ноябрь",
      "Декабрь",
    ][monthIndex];
  },

  clearCalendar: function () {
    vanillaCalendarPrev.month.innerHTML = "";
  },

  clearPrevCalendar: function () {
    vanillaCalendarPrev.prevmonth.innerHTML = "";
  },

  removeActiveClass: function () {
    for (let i = 0; i < this.activeDates.length; i++) {
      this.activeDates[i].classList.remove("vcal-date--selected");
    }
  },
};
