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

// Password show and hide Function

state = false

function showpass() {
    const passInput = document.getElementById('pass')
    const eye = document.getElementById('eye')
    if (state) {
        passInput.setAttribute('type', 'password')
        state = false
        eye.classList.add('bx-show')
        eye.classList.remove('bx-hide')
    } else {
        eye.classList.add('bx-hide')
        eye.classList.remove('bx-show')
        passInput.setAttribute('type', 'text')
        state = true
    }

}

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
        }

    }).then(result=>result.json())
    .then(response=>{
        if(response.status == 200){
            username.value=response.username
            fname.value=response.fname
            lname.value=response.lname
            email.value=response.email
            bio.value=response.bio
            countChracters(response.bio)
        }
        console.log(response)
    })

}


// Count Character of Profile bio 


function countChracters(value)
{
    const bio=document.getElementById('bio')
    let characterLen=document.getElementById('lenght')
    let bioError=document.getElementById('bio-error')
    const bioLength=value.length
    if (bioLength>150)
    {
        console.log('length exceeds',bioLength)
        bioError.classList.remove("d-none")
        bio.classList.add("disabled")
    }else{
        characterLen.innerHTML=bioLength
        bio.classList.remove("disabled")
        bioError.classList.add("d-none")
    }
}

window.onload=function(){
    try{
    const text=document.getElementById('message')
    const alert=document.getElementById('alert')
    const c=alert.classList[1]
    if (c=='alert-success'){
            text.innerHTML="Success : "       
    } else if(c=='alert-danger'){
        text.innerHTML="Error : "
    }else if(c=='alert-warning'){
        text.innerHTML="Warning : "
    }
  }
    catch{
        
    } 
}

function btnEnable(val){
    const commentCancel=document.getElementById('comment-cancel')
    const commentSubmit=document.getElementById('comment-submit')

    if (val != ''){
        commentCancel.classList.remove('disabled')
        commentSubmit.classList.remove('disabled')
    }else{
        
        commentCancel.classList.add('disabled')
        commentSubmit.classList.add('disabled')
    }

}
// comment id
var id;

// get comment data

function EditComment(val)
{
    this.id=val
    const commentCancel=document.getElementById('comment-cancel')
    const commentSubmit=document.getElementById('comment-submit')
    const comment=document.getElementById('comment'),
    commentForm=document.getElementById('comment-form')

url='/api/get-comment?id='+val
    fetch(url,{
        method :'GET',
        headers:{
            'Content-Type':'application/json',
        }

    }).then(result=>result.json())
    .then(response=>{
       if (response.status==200)
       {
           comment.value=response.comment
            commentSubmit.classList.remove('disabled')
            commentCancel.classList.remove('disabled')
            commentSubmit.innerHTML='Save'
            commentForm.addEventListener("submit",e=>{
                e.preventDefault();
            })
       }
    })

commentCancel.addEventListener('click',function (){

    commentCancel.classList.add('disabled')
    commentSubmit.classList.add('disabled')
    commentSubmit.innerHTML='Submit'
    commentForm.addEventListener("submit",e=>{
        document.location.reload
    })
})

}

// send edited comment to server

function UpdataComment()
{

    var csrf=document.getElementById('csrf').value
    var customAlert=document.getElementById('alert')
    var message=document.getElementById('message')
    var comment=document.getElementById('comment').value
    var id=this.id
    console.log(id)
    data={
        'comment': comment,
        'id':id,
    }
    url='/api/update-comment'
    fetch(url,{
        method :'POST',
        headers:{
            'Content-Type':'application/json',
            'X-Csrftoken':csrf,
        },body:JSON.stringify(data)

    }).then(result=>result.json())
    .then(response=>{
        if(response.status == 200){
            console.log(response)
            document.location.reload()
        }
        if(response.status ==500){
            customAlert.classList.remove('d-none')
            message.innerHTML=response.message   
            document.location.reload()
        }
    })
}


// =====Share Link Script========

var shareLink;
function getLink()
{
    var shareInput=document.getElementById('share-input')
    this.shareLink=window.location.href
    shareInput.value=this.shareLink
}
function CopyShareLink()
{
    let link=document.getElementById('share-input')
    console.log('this is link', link)
     /* Select the text field */
  link.select();
  link.setSelectionRange(0, 99999); /* For mobile devices */

   /* Copy the text inside the text field */
  navigator.clipboard.writeText(link.value);

  /* Alert the copied text */
  alert("Copied the text: " + link.value);
}