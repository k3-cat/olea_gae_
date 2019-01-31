function addStaff() {
    var job = prompt("分工:");
    if (job == "" || job == null) {
        return;
    }
    document.getElementById("opt").value = "A";
    document.getElementById("data").value = job;
    document.getElementById("form").submit()
}

function finishJob() {
    document.getElementById("opt").value = "F";
    document.getElementById("form").submit()
}

function setReq() {
    var req = prompt("所需人数:");
    if (req == null) {
        return;
    }
    var rePattern = /^[\d]+$/;
    if (!rePattern.test(req)) {
        alert("! 输入无效 请输入一个非负整数 !");
        return;
    }
    document.getElementById("opt").value = "R";
    document.getElementById("data").value = req;
    document.getElementById("form").submit()
}

function editJob(uid) {
    var job = prompt("分工:", document.getElementById(uid).innerHTML);
    if (job == "" || job == null) {
        return;
    }
    document.getElementById("opt").value = "E";
    document.getElementById("data").value = job;
    document.getElementById("form").submit();
}

function delStaff(event) {
    event.preventDefault();
    var name = event.dataTransfer.getData("Text");
    if (!confirm(name+" 确定要取消接稿吗?")) {
        return;
    }
    document.getElementById("opt").value = "D";
    document.getElementById("form").submit();
}

function onDragOver(event) {
    event.preventDefault();
}

function onDragEnter(event) {
    document.getElementById("delbox").style.color = "white";
    document.getElementById("delbox").style.background = "red";
}

function onDragLeave(event) {
    document.getElementById("delbox").style.color = "red";
    document.getElementById("delbox").style.background = "white";
}

function dragStart(event) {
    event.dataTransfer.effectAllowed = "move"
    document.getElementById("optbox").style.display = "none";
    document.getElementById("delbox").style.display = "block";
    event.dataTransfer.setData("Text", event.target.innerHTML);
}

function dragEnd(event) {
    document.getElementById("optbox").style.display = "grid";
    document.getElementById("delbox").style.display = "none";
}
