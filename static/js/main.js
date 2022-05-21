function login()
{
    var username=document.getElementById('loginUsername').value
    var password=document.getElementById('loginPassword').value
    var csrf=document.getElementById('csrf').value
    
    if (username =='' && password ==''){
        alert("Enter must both")
    }

    data={
        'username': username,
        'password': password,
    }
    url='/api/login'
    fetch(url,{
        method :'POST',
        headers:{
            'Content-Type':'application/json',
            'X-Csrftoken':csrf,
        },body:JSON.stringify(data)

    }).then(result=>result.json())
    .then(response=>{
        if(response.status == 200){
            window.location.href='/'
        }
    })

}