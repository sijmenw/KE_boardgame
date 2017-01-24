displayView = function(viewToDisplay){
    var newView = document.getElementById(viewToDisplay).innerHTML;
    var viewContainer = document.getElementById('viewContainer');
    viewContainer.innerHTML = newView;

    // if the view to display is the welcome screen, populate the form
    if (viewToDisplay == 'welcomeView') {
        // send to server
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange=function() {
            if (xhttp.readyState == 4) {
                JSONResultObject = JSON.parse(xhttp.responseText);
                if (JSONResultObject['success'] == 'true') {
                    // populate the form
                    console.log("options received:", JSONResultObject.data);
                    populateForm(JSONResultObject.data)
                } else {
                    // give feedback
                    console.log('ERROR: Fucked shit up');
                }
            }
        };

        xhttp.open("POST", "get_form_options/", true);
        xhttp.send();
    }

};

populateForm = function(data) {

    var checkboxKeys = Object.keys(data);

    for (var keyCount = 0; keyCount < checkboxKeys.length; keyCount++) {
        var innerHtml = "";
        var keyName = checkboxKeys[keyCount];

        var checkboxList = data[keyName];
        var title = keyName;

        for (var i = 0; i < checkboxList.length; i++) {
            innerHtml += "<div class='row'><div class='col-md-6'>" + title + "</div> <div class='col-md-6'> <input type='checkbox' name='" + keyName + checkboxList[i] + "' value='" + checkboxList[i] + "'class='rightFloat'>" + checkboxList[i] + "</div></div>"
            title = "";
        }

        document.getElementById(keyName).innerHTML = innerHtml;
    }

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
