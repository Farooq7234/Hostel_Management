const selectStaffLeaveType = document.getElementById("staffLeaveType");
const from = document.getElementById("fromDate");
const to = document.getElementById("toDate");
const daysCountFromTo = document.getElementById("daysCountFromTo");

selectStaffLeaveType.addEventListener("change", (event)=>{
    let days = parseInt(event.target.selectedOptions[0].dataset.days);

    var fd = new Date();
    var fdStr = fd.toLocaleDateString("en-CA");
    from.value = fdStr;

    var td = new Date();
    var tdPlus = td.setDate(fd.getDate() + days);
    var tdStr = td.toLocaleDateString("en-CA");
    to.value = tdStr;

    daysCountFromTo.innerHTML = `${days} Days`;
});

from.addEventListener("change", (event)=>{
    const start = from.value;
    const end = to.value;
    let diffDays = dateDiff(start, end);
    diffDays = (diffDays>0)?diffDays:"Invalid";
    daysCountFromTo.innerHTML = `${diffDays} Days`;
});

to.addEventListener("change", (event)=>{
    const start = from.value;
    const end = to.value;
    let diffDays = dateDiff(start, end);
    diffDays = (diffDays>0)?diffDays:"Invalid";
    daysCountFromTo.innerHTML = `${diffDays} Days`;
});

function dateDiff(d1, d2) {
    const oneDay = 24 * 60 * 60 * 1000;

    var startDate = new Date(d1);
    var endDate = new Date(d2);
    var diffInTime = endDate.getTime() - startDate.getTime();
    var diffInDay = diffInTime / oneDay;
    
    return diffInDay;
}