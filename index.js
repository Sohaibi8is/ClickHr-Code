function get_allusers(){
    document.getElementById("adminName").innerHTML=localStorage.getItem("userName");
    var status=localStorage.getItem("sinkData");
    console.log(status);
    if(status=="" || status=="null" || status==null || status=="none"){
        localStorage.setItem("sinkData","Read New Email");
        document.getElementById("emailSink").innerHTML="Read New Email";
    }
    else{
        document.getElementById("emailSink").innerHTML=status;
    }
    var $row = $('#row')
    $.ajax({
        headers: {
            'Content-Type': 'application/json'
        },
        type: 'GET',
        //url: 'http://162.214.195.234:8081/api/allusers',
        url : 'http://127.0.0.1:8081/api/allusers',
        success: function(data){
            data['data']=data['data'].reverse();
            // console.log(data)
            $.each(data, function(i,item) {
                $.each(this, function(i, item){
                    console.log("item =>", item)
                    var address=item.country
                    $row.append('<tr><td>' + item.id+ '</td><td>' + item.name+ '</td><td>' + item.email+   //Muhammad Sohaib
                     '</td><td>' + item.phone_number+ '</td><td>' + item.designation+ '</td><td>' + item.education +
                      '</td><td>' + item.skills+ '</td><td>' + item.experience+ '</td><td>'+ item.total_experience+ 
                      ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                       ' </td><td>' + item.job_title + '</td><td>' + item.applied_date +
                        '</td><td>' + item.screener_question+'</td></tr>');
                });

            });
        }
    });
};

function userVerification(){
    status=localStorage.getItem('userLoggedin');
    if(status=="True"){
        get_allusers();
    }
    else{
        redirectUserToSignin();
        localStorage.setItem("signinError","true");
        document.getElementById("unautorizeError").innerHTML="Unauthorized User Please Signin First to Get Access"
    }
}

function checkError(){
    status=localStorage.getItem('userLoggedin');
    if(status=="True"){
        redirectUserToDashboard();
    }
    else{
        error=localStorage.getItem("signinError");
        if(error=="true"){
            document.getElementById("unautorizeError").innerHTML="Unauthorized User Please Signin First to Get Access";
            localStorage.clear();
        }
        else{
        }
    }
}

//Filter
function filters(){
    var filter=["name","email","phoneNumber","designation","education","skills","experience","country","screenerQuestions","jobTitle","appliedDate"]
    var increment=0;
    var search=[]
    
}

//Clear Table
function clearTable(){
    var $row = $('#row');
    $row.replaceWith("<tbody id='row' onclick='rowClick()'><tr style='width: 10px'></tr></tbody>");
    submitSearchForm();
};

//Serach Data
function submitSearchForm(){
    var searchData=document.getElementById("searchData").value;
    var elements=document.getElementsByName("searchBy");
    var searchBy=""
    for(i = 0; i < elements.length; i++) {
        if(elements[i].checked){
            searchBy = "searchBy: "+elements[i].value;
        }
    }
    var value = searchBy.split(" ");
    apiTransferData=[searchData,value[1]]
    console.log(apiTransferData)
    if(searchData=="" || searchData==null){
        var $row = $('#row');
        $.ajax({
            headers: {
                'Content-Type': 'application/json'
            },
            type: 'GET',
            //url: 'http://162.214.195.234:8081/api/allusers',
            url : 'http://127.0.0.1:8081/api/allusers',
            success: function(data){
                // console.log(data)
                $.each(data, function(i,item) {
                    $.each(this, function(i, item){
                        console.log("item =>", item)
                        var address=item.country
                        $row.append('<tr><td>' + item.id+ '</td><td>' + item.name+ '</td><td>' + item.email+   //Muhammad Sohaib
                         '</td><td>' + item.phone_number+ '</td><td>' + item.designation+ '</td><td>' + item.education +
                          '</td><td>' + item.skills+ '</td><td>' + item.experience+ '</td><td>'+ item.total_experience+ 
                          ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                           ' </td><td>' + item.job_title + '</td><td>' + item.applied_date +
                            '</td><td>' + item.screener_question+'</td></tr>');
                    });
    
                });
            }
        });
    }
    else{
    var $row = $('#row');
    $.ajax({
        headers: {
            'Content-Type': 'application/json'
        },
        type: 'GET',
        //url: "http://162.214.195.234:8081/api/searchObject/" +apiTransferData,
        url : 'http://127.0.0.1:8081/api/searchObject/'+apiTransferData,
        success: function(data){
            // console.log(data)
            $.each(data, function(i,item) {
                $.each(this, function(i, item){
                    //console.log("item =>", item)
                    var address=item.country
                    $row.append('<tr><td>' + item.id+ '</td><td>' + item.name+ '</td><td>' + item.email+   //Muhammad Sohaib
                     '</td><td>' + item.phone_number+ '</td><td>' + item.designation+ '</td><td>' + item.education +
                      '</td><td>' + item.skills+ '</td><td>' + item.experience+ '</td><td>'+ item.total_experience+ 
                      ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                       ' </td><td>' + item.job_title + '</td><td>' + item.applied_date +
                        '</td><td>' + item.screener_question+'</td></tr>');
                    });

                });
            }
        });
    }
}

//Master Search
function masterSearchForm(data){
    var searchData=data
    apiTransferData=[data,"all"]
    console.log(apiTransferData);
    if(searchData=="" || searchData==null){
        var $row = $('#row');
        $.ajax({
            headers: {
                'Content-Type': 'application/json'
            },
            type: 'GET',
            //url: 'http://162.214.195.234:8081/api/allusers',
            url : 'http://127.0.0.1:8081/api/allusers',
            success: function(data){
                // console.log(data)
                $.each(data, function(i,item) {
                    $.each(this, function(i, item){
                        console.log("item =>", item)
                        var address=item.country
                        $row.append('<tr><td>' + item.id+ '</td><td>' + item.name+ '</td><td>' + item.email+   //Muhammad Sohaib
                         '</td><td>' + item.phone_number+ '</td><td>' + item.designation+ '</td><td>' + item.education +
                          '</td><td>' + item.skills+ '</td><td>' + item.experience+ '</td><td>'+ item.total_experience+ 
                          ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                           ' </td><td>' + item.job_title + '</td><td>' + item.applied_date +
                            '</td><td>' + item.screener_question+'</td></tr>');
                    });
    
                });
            }
        });
    }
    else{
    var $row = $('#row');
    $.ajax({
        headers: {
            'Content-Type': 'application/json'
        },
        type: 'GET',
        //url: "http://162.214.195.234:8081/api/searchObject/" +apiTransferData,
        url : 'http://127.0.0.1:8081/api/searchObject/'+apiTransferData,
        success: function(data){
            // console.log(data)
            $.each(data, function(i,item) {
                $.each(this, function(i, item){
                    //console.log("item =>", item)
                    var address=item.country
                    $row.append('<tr><td>' + item.id+ '</td><td>' + item.name+ '</td><td>' + item.email+   //Muhammad Sohaib
                     '</td><td>' + item.phone_number+ '</td><td>' + item.designation+ '</td><td>' + item.education +
                      '</td><td>' + item.skills+ '</td><td>' + item.experience+ '</td><td>'+ item.total_experience+ 
                      ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                       ' </td><td>' + item.job_title + '</td><td>' + item.applied_date +
                        '</td><td>' + item.screener_question+'</td></tr>');
                    });

                });
            }
        });
    }
}

// get field name to make dynamic url
// function changeName(e) {tru
// }
var field = ""
function selectField() {
    // if((document.getElementById("checkbox1").checked == true || document.getElementById("checkbox2").checked == true || document.getElementById("checkbox3").checked == true || document.getElementById("checkbox4").checked == true || document.getElementById("checkbox5").checked == true || document.getElementById("checkbox6").checked == true || document.getElementById("checkbox7").checked == true || document.getElementById("checkbox8").checked == true) && (document.getElementById("checkbox2").checked == true || document.getElementById("checkbox3").checked == true || document.getElementById("checkbox4").checked == true || document.getElementById("checkbox5").checked == true || document.getElementById("checkbox6").checked == true || document.getElementById("checkbox7").checked == true || document.getElementById("checkbox8").checked == true)){  
    //     return document.getElementById("error").innerHTML = "Please mark only one checkbox";  
    //   }
        if (document.getElementById("checkbox1").checked == true){

            document.getElementById("checkbox2").checked = false
            //console.log("value of checkbo 2", document.getElementById("checkbox2").checked )
            document.getElementById("checkbox3").checked = false
            document.getElementById("checkbox4").checked = false
            document.getElementById("checkbox5").checked = false
            document.getElementById("checkbox6").checked = false
            document.getElementById("checkbox7").checked = false
            document.getElementById("checkbox8").checked = false
            document.getElementById("checkbox9").checked = false
            document.getElementById("checkbox10").checked = false
            document.getElementById("checkbox11").checked = false

            field = document.getElementById("checkbox1").value;
        // console.log("field => ", field)
        }  

        else if ( email = document.getElementById("checkbox2").checked == true){  
            field = document.getElementById("checkbox2").value; 
        }

        else if (document.getElementById("checkbox3").checked == true){  
            field = document.getElementById("checkbox3").value; 
        }  

        else if (document.getElementById("checkbox4").checked == true){  
            field = document.getElementById("checkbox4").value; 
        }  

        else if (document.getElementById("checkbox5").checked == true){  
            field = document.getElementById("checkbox5").value; 
        }  

        else if (document.getElementById("checkbox6").checked == true){  
            field = document.getElementById("checkbox6").value;
        }  

        else if (document.getElementById("checkbox7").checked == true){  
            field = document.getElementById("checkbox7").value; 
        }

        else if (document.getElementById("checkbox8").checked == true){  
            field = document.getElementById("checkbox8").value; 
        }

        else if (document.getElementById("checkbox9").checked == true){  
            field = document.getElementById("checkbox9").value; 
        }

        else if (document.getElementById("checkbox10").checked == true){  
            field = document.getElementById("checkbox10").value; 
        }

        else if (document.getElementById("checkbox11").checked == true){  
            field = document.getElementById("checkbox11").value; 
        }


        else { 
        field = "";  
        }  
  }


// get input parameter
var fieldValue = ""
function changeValue(e) {
    fieldValue = e.value
}


// read new emails and update database
function FetchEmail(){
    localStorage.setItem("sinkData","Loading...")
    document.getElementById("emailSink").innerHTML="Loading...";
    $.ajax({
        type: "GET",
        //url: "http://162.214.195.234:8081/api/refresh_page",
        url : 'http://127.0.0.1:8081/api/refresh_page',
        success: function(data) {
            localStorage.setItem("sinkData","Read New Email");
            document.getElementById("emailSink").innerHTML="Read New Email";
            alert("Data Fetched...");
            location.reload();
        }
    });
}



function buttonClick(){
    selectField();

   // console.log("field selected => ", field)

    // clear rows data first
    $("tbody#row tr").remove()
    
    var $row = $('#row')
    
    if (field) {
    $.ajax({
    type: "POST",
    //url: "http://162.214.195.234:8081/api/" + field,
    url : 'http://127.0.0.1:8081/api/'+field,
    data: {value: fieldValue},
    success: function(data) {
        //console.log(data)

        $.each(data, function(i, item) {
            $.each(this, function(i, item){
                var address=item.country
                $row.append('<tr><td>'+ item.id+ '</td><td>'+ item.name +'</td><td>'+ item.email+  //Muhammad Sohaib
                ' </td><td>'+ item.phone_number+' </td><td> '+ item.designation+' </td><td> '+ 
                item.education+' </td><td> '+ item.skills+' </td><td> '+ item.experience+' </td><td>'+
                 item.total_experience+' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+
                  item.country+'</td><td>'+ item.job_title+' </td><td>'+ item.applied_date+' </td><td> '+
                   item.screener_question+'</td></tr>');

            });

        });
    }
    });

} else{

    $.ajax({
        type: "POST",
        //url: "http://162.214.195.234:8081/api/custom_api",
        url : 'http://127.0.0.1:8081/api/custom_api',
        data: {value: fieldValue},
        success: function(data) {
           // console.log(data)
            $.each(data, function(i, item) {
                $.each(this, function(i, item){
                    $row.append('<tr><td>'+ item.id+ '</td><td>'+ item.name +'</td><td>'+ item.email+' </td><td>'+ //Muhammad Sohaib
                    item.phone_number+' </td><td> '+ item.designation+' </td><td> '+ item.education+' </td><td> '+ 
                    item.skills+' </td><td> '+ item.experience+' </td><td>'+ item.total_experience+
                    ' </td><td style="cursor:pointer" onclick="newClick(\'' + item.country + '\')">'+ item.country+
                     ' </td><td>'+ item.job_title+' </td><td>'+ item.applied_date +' </td><td> '+
                      item.screener_question+ '</td></tr>');
                });

            });
        }
        });
    }
}




function pdf_file(){
    file_path = localStorage.getItem("file_path")
  //  console.log ("file_path". file_path)
    document.getElementById('filePath').setAttribute("src","https://"+file_path);
   // console.log ("file_path set ", file_path)
}


var userID = ""
function rowClick(){
   // console.log("Row is clicked")

    var table = document.getElementById('table') 
    var cells = table.getElementsByTagName('td');

    for (var i = 0; i < cells.length; i++) {
        // Take each cell
        var cell = cells[i];
        // do something on onclick event for cell
        cell.onclick = function () {
            // Get the row id where the cell exists
            var rowId = this.parentNode.rowIndex;

            var rowsNotSelected = table.getElementsByTagName('tr');
            for (var row = 0; row < rowsNotSelected.length; row++) {
                rowsNotSelected[row].style.backgroundColor = "";
                rowsNotSelected[row].classList.remove('selected');
            }

            var rowSelected = table.getElementsByTagName('tr')[rowId];
            //rowSelected.style.backgroundColor = "yellow";
            rowSelected.className += "selected";
            userID = rowSelected.cells[0].innerHTML;
            console.log(rowSelected);
            console.log("userID => ", userID);
            localStorage.setItem("userID",userID);
            location.replace('profile.html')
        }
    }


}



// console.log(userID)
function info(userID){
    document.getElementById("adminName").innerHTML=localStorage.getItem("userName");
    document.getElementById("commentBox").style.backgroundColor="none";
    id = localStorage.getItem("userID");
   console.log("function onload runned with user ID : ", id);
    var $row = $('#row');
    $.ajax({
        type: "POST",
        //url: "http://162.214.195.234:8081/api/user/" + id,
        url : 'http://127.0.0.1:8081/api/user/'+id,
        data: {value: fieldValue},
        success: function(data) {
          //  console.log("data fetched: ", data)

            // location.replace('profile.html')

            $.each(data, function(i, item) {
                $.each(this, function(i, item){
                    console.log(item)
                    if(item.education!="null"){
                        document.getElementById("titleProfession").innerHTML= " - " + item.education
                    }
                    document.getElementById('titleName').innerHTML=item.name
                    document.getElementById('name').innerHTML = item.name
                    localStorage.setItem("applicantName",item.name)
                    document.getElementById('email').innerHTML = item.email
                    localStorage.setItem("applicantEmail",item.email)
                    document.getElementById('phoneNumber').innerHTML = item.phone_number
                    document.getElementById('skills').innerHTML = item.skills
                    document.getElementById('designation').innerHTML = item.designation
                    document.getElementById('education').innerHTML = item.education
                    document.getElementById('experience').innerHTML = item.experience
                    document.getElementById('totalExperience').innerHTML = item.total_experience
                    console.log(item.country,item)
                    document.getElementById('country').innerHTML = item.country
                    document.getElementById('jobtitle').innerHTML = item.job_title
                    document.getElementById('appliedDate').innerHTML = item.applied_date
                    document.getElementById('screenerQuestion').innerHTML = item.screener_question
                    document.getElementById('status').innerHTML = item.status
                    document.getElementById('joinDate').innerHTML = item.join_date
                    document.getElementById('agent').innerHTML = item.agent
                    
                    file_path  = item.resume_filepath 
                    localStorage.setItem("file_path", file_path);

                    localStorage.setItem("eidtName",item.name);
                    localStorage.setItem("editEmail",item.email);
                    localStorage.setItem("editPhoneNumber",item.phone_number);
                    localStorage.setItem("editSkills",item.skills);
                    localStorage.setItem("editDesignation",item.designation);
                    localStorage.setItem("editEducation",item.education);
                    localStorage.setItem("editExperience",item.experience);
                    localStorage.setItem("editTotalExperience",item.total_experience);
                    localStorage.setItem("editCountry",item.country);
                    localStorage.setItem("editJobTitle",item.job_title);
                    localStorage.setItem("editScreenerQuestion",item.screener_question);

                    // document.getElementById('filePath').setAttribute("src",item.resume_filepath);

                    // document.getElementById('download').href = item.resume_filepath
                    
                    
                    // document.getElementById("btn") 
                    //     .addEventListener("download", function() { 
                    //     // Generate download of hello.txt  
                    //     // file with some content 
                    //     var text = document.getElementById("text").value; 
                    //     var filename = "GFG.txt"; 
                    
                    //     download(filename, text); 
                    // }, false); 

                });

            });
            fetchComments();
        }
        });
        
}
function newClick(address){                 //Muhammad Sohaib
  //  console.log(address);
    //window.open("http://162.214.195.234:8081/api/location/"+address,'_self');
    window.open("http://127.0.0.1:8081/api/location/"+address,'_self');
}


// //SignIn Form Validation
// function UsernameValidation(){
//     username=document.getElementById("signinUsername").value;
//     console.log(username);
//     test1=username.match(/[A-Z]/g);
//     test2=username.match(/[0-9]/g);
//     test3=username.match(/[a-z]/g);
//     console.log(test1);
//     console.log(test2);
//     console.log(test3);
//     document.getElementById("signinUsernameValidate").innerHTML="The username must be consist of one capitial,one small and one number";
//     if(username==""){
//         console.log(username);
//         // console.log(isUpper(username));
//     }
//     else{
//         document.getElementById("signinUsernameValidate").innerHtml="The username must be consist of one capitial,one small and one number";
//     }
// }

//SigninForm
function verifyUser(){
        localStorage.clear();
        var username=document.getElementById("signinUsername").value;
        var password=document.getElementById("signinPassword").value;
        if(username=="" || password==""){
            document.getElementById("signinPasswordValidate").innerHTML = "Fill all required fields";
        }
        else{
        var userData=[username,password]
        console.log(userData);
        $.ajax({
            headers: {
                'Content-Type': 'application/json'
            },
            type: 'GET',
            //url: 'http://162.214.195.234:8081/api/userLogin/'+userData,
            url : 'http://127.0.0.1:8081/api/userLogin/'+userData,
            success: function(data){
                document.getElementById("signinUsernameValidate").innerHTML = "";
                document.getElementById("signinPasswordValidate").innerHTML="";
                console.log(data);
                if(data["result"]=="success"){
                    document.getElementById("signinButton").style.color="green";
                    localStorage.setItem("userName",username);
                    document.getElementById("signinButton").innerHTML="Success...";
                    document.getElementById("signinUsernameValidate").innerHTML = "<div class='loader'></div>";
                    //console.log("done");
                    localStorage.setItem('userLoggedin',"True");
                    localStorage.setItem('sinkData',"Read New Email");
                    setTimeout(redirectUserToDashboard,2000);
                }
                else if(data["result"]=="Invalid Password"){
                    document.getElementById("signinPasswordValidate").innerHTML = "Invalid Password";
                }
                else{
                    document.getElementById("signinUsernameValidate").innerHTML = "Invalid Username";
                } 
            }
        });
        }
};

function userLogout(){
    localStorage.clear();
    redirectUserToSignin();
}

// function redirectUserToDashboard(){
//     window.location.href = "http://addats.com/html/dashboard-3.html";
// }
// function redirectUserToSignin(){
//     window.location.href = "http://addats.com/html/sign-in.html";
// }

function redirectUserToDashboard(){
    window.location.href = "dashboard-3.html";
}
function redirectUserToSignin(){
    window.location.href = "sign-in.html";
}

function addNewApplicantData(){
    var name=document.getElementById("applicantName").value;
    var email=document.getElementById("applicantEmail").value;
    var phoneNumber=document.getElementById("applicantPhone").value;
    var designation=document.getElementById("applicantDesignation").value;
    var education=document.getElementById("applicantEducation").value;
    var skills=document.getElementById("applicantSkills").value;
    var experience=document.getElementById("applicantExperience").value;
    var country=document.getElementById("applicantCountry").value;
    var total_experience=document.getElementById("applicantTotalExperience").value;
    var address=document.getElementById("applicantAddress").value;
    var job_title=document.getElementById("applicantAppliedJobTitle").value;
    var screener_question=document.getElementById("applicantScreenerQuestion").value;
    var resumeName=document.getElementById("UploadResume").value;
    var resumeNameSplitted = resumeName.split("\\");
    var finalResumeName = resumeNameSplitted[resumeNameSplitted.length-1];
    const resume =document.getElementById("UploadResume").files[0];
    var applicantData=[name,email,phoneNumber,designation,education,skills,experience,country,total_experience,address,job_title,screener_question,finalResumeName];
    if(name==""||name==null||email==""||email==null||designation==""||phoneNumber==null||phoneNumber==""||designation==null||education==""||education==null||skills==""||skills==null||experience==""||experience==null||country==""||country==null||total_experience==""||total_experience==null||address==""||address==null||job_title==""||job_title==null||screener_question==""||screener_question==null||resumeName==""||resumeName==null){
        document.getElementById("addManualApplicantError").innerHTML="Fill all required fields";
    }
    else{
    var formData=resume;
    console.log(formData);
    $.ajax({
        //url: "http://162.214.195.234:8081/api/addApplicantManually/'+applicantData",
        url : 'http://127.0.0.1:8081/api/addApplicantManually/'+applicantData,
        type: "POST",
        caches:false,
        contentType:false,
        processData:false,
        data:{'file':formData},
        success: function(response) {
            alert("Inserted...");
            location.reload();
        }
    });
    }
}

function insertComment(){
    userName=localStorage.getItem("userName");
    applicantEmail=localStorage.getItem("applicantEmail");
    comment=document.getElementById("userComment").value;
    if(comment==""){
        document.getElementById("commentBox").style.backgroundColor="red";
    }
    else{
    data=[userName,applicantEmail,comment];
    console.log(data);
    $.ajax({
        //url: "http://162.214.195.234:8081/api/insertComment/'+data",
        url : 'http://127.0.0.1:8081/api/insertComment/'+data,
        type: "POST",
        success: function(response) {
            location.reload();
        }
    });
}
}

function fetchComments(){
    applicantEmail=localStorage.getItem("applicantEmail");
    document.getElementById("applicantCommentNotes").innerHTML="";
    console.log(applicantEmail);
    $.ajax({
        type: "GET",
        //url: "http://162.214.195.234:8081/api/fetchComments/'+applicantEmail",
        url : 'http://127.0.0.1:8081/api/fetchComments/'+applicantEmail,
        headers: {
            'Content-Type': 'application/json'},
        success: function(response) {
            data=response.result;
            data=data.reverse();
            $.each(data, function(i,item) {
                console.log(item);
                $("#applicantCommentNotes").append('<div class="d-flex justify-content-center py-2"><div class="second_comment py-2 px-2"> <span class="text1_comment">'+item[2]+'</span><div class="d-flex justify-content-between py-1 pt-2"><div><img src="images/demoUserCommentImage.png" width="18"><span class="text2_comment">'+item[0]+'</span></div><div><span class="text3_comment">'+item[3]+'</span><span class="thumbup"></span><span class="text4_comment">'+item[4]+'</span></div></div></div></div>');
            });
        }
    });
}

function editApplicantDetail(){
    console.log("edit Applicant Details");
    name=document.getElementById("applicantName").value;
    email=document.getElementById("applicantEmail").value;
    phone=document.getElementById("applicantPhone").value;
    designation=document.getElementById("applicantDesignation").value;
    education=document.getElementById("applicantEducation").value;
    skills=document.getElementById("applicantSkills").value;
    experience=document.getElementById("applicantExperience").value;
    country=document.getElementById("applicantCountry").value;
    totalExperience=document.getElementById("applicantTotalExperience").value;
    jobTitle=document.getElementById("applicantAppliedJobTitle").value;
    sq=document.getElementById("applicantScreenerQuestion").value;

    dataPost=String([name,"$"+email,"$"+phone,"$"+designation,"$"+education,"$"+skills,"$"+experience,"$"+country,"$"+totalExperience,"$"+jobTitle,"$"+sq]);
    console.log(data);
    $.ajax({
        //url: "http://162.214.195.234:8081/api/editApplicantDetails/",
        url : 'http://127.0.0.1:8081/api/editApplicantDetails/',
        type: "POST",
        contentType: 'application/json;charset=UTF-8',
        data:dataPost,
        headers: {
            'Content-Type': 'application/json'
        },
        success: function(response){
            alert("Information Updated!...");
            location.reload();
        }
    });  
}

function deleteApplicantInfo(){
    email=localStorage.getItem("applicantEmail");
    console.log(email);
    $.ajax({
        //url: "http://162.214.195.234:8081/api/deleteApplicantInfo/"+email,
        url:"http://127.0.0.1:8081/api/deleteApplicantInfo/"+email,
        tyoe:'POST',
        success:function(response){
            console.log(response);
            redirectUserToDashboard();
        }
    });
}