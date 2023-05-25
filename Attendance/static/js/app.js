var dt = new Date();

function RenderDate(){
    dt.setDate(1);
    var day = dt.getDay();
    var endDate = new Date(
        dt.getFullYear(),
        dt.getMonth() + 1,
        0
    ).getDate();

    var prevDate = new Date(
        dt.getFullYear(),
        dt.getMonth(),
        0
    ).getDate();

    var today = new Date();

    
    var months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ];
    // console.log(months[dt.getMonth()]);

    var options = { weekday: 'long', year: 'numeric', day: 'numeric' };
    var formattedDate = dt.toLocaleDateString('en-IN', options);
    formattedDate = formattedDate.replace(/\b(\d)(?!\d)\b/g, "$1,");
    document.getElementById("date_str").innerHTML = formattedDate;
    
    // document.getElementById("date_str").innerHTML = dt.toDateString();
    document.getElementById("month").innerHTML = months[dt.getMonth()];

    var cells = "";

    for(x=day; x>0; x--){
        cells+= "<div class='prev_date'>" + (prevDate - x + 1) + "</div>";
    }

    for(i=1; i<=endDate; i++){
        if(i == today.getDate() && dt.getMonth() == today.getMonth()){
            cells+= "<div class='today'>" + i + "</div>";
        }
        else{
            cells+= "<div>" + i + "</div>";
        }
    }

    // Get the remaining number of cells to fill with the dates of the next month
    var remainingCells = 42 - (day + endDate);

    // Retrieve the next month's information
    var nextMonthDate = new Date(dt.getFullYear(), dt.getMonth() + 1, 1);
    var nextMonthEndDate = new Date(
        nextMonthDate.getFullYear(),
        nextMonthDate.getMonth() + 1,
        0
    ).getDate();

    // Display the dates of the next month
    for (j = 1; j <= remainingCells; j++) {
        cells += "<div class='prev_date'>" + j + "</div>";
    }

    document.getElementsByClassName("days")[0].innerHTML = cells;
}

function moveDate(para){
    if(para == 'prev'){
        dt.setMonth(dt.getMonth() - 1);
    }
    else if(para == 'next'){
        dt.setMonth(dt.getMonth() + 1);
    }
    RenderDate();
}