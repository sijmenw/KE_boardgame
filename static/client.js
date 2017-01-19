displayView = function(viewToDisplay){
    var newView = document.getElementById(viewToDisplay).innerHTML;
    var viewContainer = document.getElementById('viewContainer');
    viewContainer.innerHTML = newView;
};

processQuery = function() {
    var queryForm = document.getElementById('queryForm');
    var parsedForm = parseFormObject(queryForm);
    var JSONForm = objectToJSON(parsedForm);

    // send to server
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
        if (xhttp.readyState == 4) {
            JSONResultObject = JSON.parse(xhttp.responseText);
            if (JSONResultObject['success'] == 'true') {
                var resultString = JSONResultObject['data'];
                console.log(resultString);
                displayView('resultView');
                document.getElementById('results').innerHTML = resultString;
            } else {
                // give feedback
                console.log('ERROR: Fucked shit up');
            }
        }
    };

    xhttp.open("POST", "query_games/", true);
    xhttp.send(JSONForm);
};

window.onload = function(){
    var viewToDisplay = 'welcomeView';

    displayView(viewToDisplay);
};

objectToJSON = function(inputObject) {
    jsonString = "{";
    for (var key in inputObject) {
        // keys without a name will be skipped
        if (inputObject.hasOwnProperty(key) && key != "") {
            jsonString += "\"" + key + "\":\"" + inputObject[key] + "\", ";
        }
    }
    jsonString = jsonString.slice(0,-2);
    jsonString += "}";
    return(jsonString);
};

parseFormObject = function(inputObject) {
    var resultObject = new Object();
    for (var key in inputObject) {
        if (inputObject.hasOwnProperty(key)) {
            resultObject[inputObject[key].name] = inputObject[key].value;
        }
    }
    return resultObject;
};
