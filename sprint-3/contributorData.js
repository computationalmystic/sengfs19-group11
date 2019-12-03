function getContrData(group) {
        
    var group = group;
    console.log(group);
    
    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "http://129.114.16.76:5000/api/unstable/repo-groups/" + group + "/contributor-affiliation/", true);
    
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            console.log(data);
            
            // UPDATE TABLE HERE
        } 
    };

    xhttp.send();
    
}