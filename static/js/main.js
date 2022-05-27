/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
    const header = document.getElementById('navigation')
    if (this.scrollY >= 50) {
        header.classList.add('scroll-header');
    } else {

        header.classList.remove('scroll-header')
    }

}
window.addEventListener('scroll', scrollHeader)

function loginWithEnter()
{
    var pass=document.getElementById('loginPassword')
    pass.addEventListener("keypress",function(event){
        if (event.key === "Enter"){
            event.preventDefault();

                document.getElementById('login-btn').click()
        }
    })
}


// Add class for active navbar links

window.addEventListener("load",e=>{
    let text = window.location;
    console.log(text.stringify)
})

// getting year for footer

window.addEventListener("load",function (){
    const year=document.getElementById('year')
    today=new Date()
    year.innerHTML=today.getFullYear()
})

function login()
{
    var username=document.getElementById('loginUsername').value
    var password=document.getElementById('loginPassword').value
    var csrf=document.getElementById('csrf').value
    var customAlert=document.getElementById('alert')
    var message=document.getElementById('message')
    
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
            customAlert.classList.remove('d-none')
         message.innerHTML=response.message   
        }
    })

}

function register()
{
    var customAlert=document.getElementById('alert')
    var message=document.getElementById('message')
    var username=document.getElementById('registerUsername').value
    var fname=document.getElementById('fname').value
    var lname=document.getElementById('lname').value
    var email=document.getElementById('email').value
    var password=document.getElementById('registerPassword').value
    var csrf=document.getElementById('csrf').value
    const inputGroup=document.querySelectorAll('.form-control')
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
            // 'X-Csrftoken':csrf,
        },body:JSON.stringify(data)

    }).then(result=>result.json())
    .then(response=>{
        console.log(response)
        if(response.status == 200){
          
        }
        
    })

}

function editProfile(){
    let username=document.getElementById('username')
    let fname=document.getElementById('fname')
    let lname=document.getElementById('lname')
    let email=document.getElementById('email')
    let bio=document.getElementById('bio')
    url='/api/get-profile'
    fetch(url,{
        method :'GET',
        headers:{
            'Content-Type':'application/json',
            // 'X-Csrftoken':csrf,
        }

    }).then(result=>result.json())
    .then(response=>{
        if(response.status == 200){
            username.value=response.username
            fname.value=response.fname
            lname.value=response.lname
            email.value=response.email
            bio.value=response.bio
    
        }
        console.log(response)
    })

}