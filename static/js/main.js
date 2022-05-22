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
        if(response.status ==500){
            alert(response.message)
        }
    })

}

function register()
{
    var username=document.getElementById('loginUsername').value
    var fname=document.getElementById('fname').value
    var lname=document.getElementById('lname').value
    var email=document.getElementById('email').value
    var password=document.getElementById('loginPassword').value
    var csrf=document.getElementById('csrf').value
    if (username =='' && password ==''){
        alert("Enter must both")
    }

    data={
        'username': username,
        'fname': fname,
        'lname': lname,
        'email': email,
        'password': password,
    }
    url='/api/register'
    fetch(url,{
        method :'POST',
        headers:{
            'Content-Type':'application/json',
            'X-Csrftoken':csrf,
        },body:JSON.stringify(data)

    }).then(result=>result.json())
    .then(response=>{
        console.log(response)
        if(response.status == 200){
            // window.location.href='/'
            alert(response.message)
            username.value=''
            fname.value=''
            lname.value=''
            email.value=''
            password.value=''
        }
    })

    console.log(username)
    console.log(fname)
    console.log(lname)
    console.log(email)
    console.log(password)

}