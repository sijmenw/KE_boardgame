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
        var keyName = checkboxKeys[keyCount];
        var checkboxList = data[keyName];

        var title = keyName;

        var innerHtml = "";

        for (var i = 0; i < checkboxList.length; i++) {
            if (i % 3 == 0) {
                if (i > 0) {
                    innerHtml += "</div>";
                }
                innerHtml += "<div class='row'>";
            }
            innerHtml += "<div class='col-md-4'> <input type='checkbox' name='" + title + "' value='" + checkboxList[i] + "' class='rightFloat'>" + checkboxList[i] + "</div>";
        }

        innerHtml += "</div>";

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
                var recommendations = parseRecommendations(resultString);
                displayView('resultView');
                document.getElementById('results').innerHTML = recommendations;
            } else {
                // give feedback
                console.log('ERROR: Fucked shit up');
            }
        }
    };

    xhttp.open("POST", "query_games/", true);
    xhttp.send(JSONForm);
};

parseRecommendations = function(input_array) {
    var result = "<div class='row'><div class='col-md-1'></div><div class='col-md-7'>Name</div><div class='col-md-3'>User rating</div><div class='col-md-1'>Link</div></div>";
    for (var i = 0; i < input_array.length; i++) {
        var link = "<a href='https://boardgamegeek.com/boardgame/" + input_array[i].boardgame_id + "/'> BGG </a>";
        result += "<div class='row'><div class='col-md-1'>" + (i+1) + ".</div><div class='col-md-7'>" +  input_array[i].name + "</div><div class='col-md-3'>" + input_array[i].rating + "</div><div class='col-md-1'>" + link + "</div></div>";
    }
    return result;
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
    var resultObject = {};
    for (var key in inputObject) {
        if (inputObject.hasOwnProperty(key)) {
            resultObject[inputObject[key].name] = inputObject[key].value;
        }
    }

    var categoriesArray =  $("input[name='categories']:checked").map(function(){
        return this.value;
    }).get();

    var mechanicsArray =  $("input[name='mechanics']:checked").map(function(){
        return this.value;
    }).get();

    resultObject.categories = categoriesArray;
    resultObject.mechanics = mechanicsArray;

    return resultObject;
};

showOptions = function(id) {
    var selector = '#' + id;
    var buttonSelector = selector + 'Button';
    var current = $(selector).css("display");

    if (current == "none") {
        $(selector).css("display", "");
        $(buttonSelector).val("hide");
    } else {
        $(selector).css("display", "none");
        $(buttonSelector).val("show");
    }
};
