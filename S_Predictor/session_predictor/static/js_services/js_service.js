class SelectSessionActivator
{
    constructor(){}
    InitService()
        {
            var cells = document.getElementsByClassName("session-row");
            var selecting_element = document.getElementById("select-session");
            var redact_button = document.getElementById("redact-session");
            for(var k=0;k<cells.length;k++) {
                cells[k].onmouseover = function(event){
                    var target = event.target
                    var selectcells = document.getElementsByName(target.getAttribute("name"));
                    for(var n=0;n<selectcells.length;n++){
                        selectcells[n].style.background = 'lightblue';
                        }
                    }
                cells[k].onmouseout = function(event){
                    var target = event.target
                    var selectcells = document.getElementsByName(target.getAttribute("name"));
                    for(var n=0;n<selectcells.length;n++){
                    if(target.getAttribute("name") != selecting_element.getAttribute("value")){
                        selectcells[n].style.background = 'white';
                        }
                        else {
                        selectcells[n].style.background = '#3B71CA';
                        }
                    }
                }
                cells[k].onclick = function(event){
                    for(var c=0;c<cells.length;c++) {
                        cells[c].style.background = 'white';
                        }
                    var target = event.target
                    var selectrow = document.getElementsByName(target.getAttribute("name"));
                    for(var n=0;n<selectrow.length;n++){
                        selectrow[n].style.background = '#3B71CA';
                        }
                    selecting_element.setAttribute("value",target.getAttribute("name"));
                    redact_button.removeAttribute("disabled");
                    }
            }
        }
}