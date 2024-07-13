function sendData() { 
    var value = document.getElementById('input'); 
    
    
    if (value.checked){
        var number = 'followed';
        document.getElementById("follow_text").innerHTML = "Followed";
     
    } else {
        
        var number = 'unfollowed';
        document.getElementById("follow_text").innerHTML = "Follow";
    }
    $.ajax({ 
        url: '', 
        type: 'POST', 
        data: { 'data': number }, 
        
        error: function(error) { 
            console.log(error); 
        } 
    });
} 