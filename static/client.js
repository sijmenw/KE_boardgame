displayView = function(viewToDisplay){
    var newView = document.getElementById(viewToDisplay).innerHTML;
    var viewContainer = document.getElementById('viewContainer');
    viewContainer.innerHTML = newView;
};

processQuery = function() {
    var min_players = document.getElementById('queryForm').min_players.value;
    var max_players = document.getElementById('queryForm').max_players.value;
    min_players == "" ? min_players = 0 : min_players = min_players;
    max_players == "" ? max_players = 0 : max_players = max_players;

    // send to server
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
        if (xhttp.readyState == 4) {
            JSONResultObject = JSON.parse(xhttp.responseText);
            if (JSONResultObject['success'] == 'true') {
                var resultString = JSONResultObject['data'];
                console.log(resultString);
                displayView('resultView');
                document.getElementById('queryResults').innerHTML = resultString;
            } else {
                // give feedback
                document.getElementById('feedbackBox').innerHTML = 'ERROR: Fucked shit up';
            }
        }
    };
    xhttp.open("GET", "query_games/"+min_players+"/"+max_players, true);
    xhttp.send();
};

window.onload = function(){
    var viewToDisplay = 'welcomeView';

    displayView(viewToDisplay);
};
