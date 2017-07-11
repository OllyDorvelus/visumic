/**
 * Created by OllyD on 3/17/2017.
 */
//if ($('#wrapper').hasClass("menuNotDisplayed")){
//    Cookies.set("menuOutB","false");
//}
//else{
//    Cookies.set("menuOutB","true");
//}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


console.log(localStorage.getItem("sideOpen"))

//global functions withload doc ready
    function getParameterByName(name, url) {
        if (!url) {
            url = window.location.href;
        }
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

        //function attachProfile(profileValue, prepend) {
        //    var profileUser = profileValue.user
        //    var verb = "Follow"
        //    var follower_count = profileValue.follower_count
        //    if(profileValue.is_following) {
        //        verb = "Unfollow"
        //    }
        //    var profileFormattedHtml = "<div class=\"media\"><div class=\"media-body\">" +  "<br> via <a href='" + profileUser.url + "'>" +
        //            profileUser.username + " videos: " + profileUser.video_count + "</a> | " +  " | " + "<a href='#'>View "  +  "  | <a href='#' class='follow-btn btn btn-primary' data-id=" + profileValue.id + ">" + verb + " " + profileValue.follower_count + "</a></div></div><hr>"
        //
        //
        //    var profileFormattedHtml2 = "<div class='col-md-3 profilecontainer text-center'>'" +
        //            "<a href ='" +  profileUser.url + "'><img src='" + profileValue.user_img + "'class='listpic img-circle img-responsive'></a><h6>" + profileUser.username + "|</h6><span class='glyphicon glyphicon-user' aria-hidden='true'></span><h6><a href='#' class='follow-btn btn btn-primary btn-sm' data-id="+ profileValue.id +">" + verb + " " +  profileValue.follower_count + "" +
        //            "</a></h6><span class='glyphicon glyphicon-play' aria-hidden='true'></span><h6>Videos:" + profileUser.video_count + "</h6></div>"
        //    if (prepend == true) {
        //        $("#profile-container").prepend(profileFormattedHtml)
        //    }
        //    else {
        //        $("#profile-container").append(
        //                profileFormattedHtml2
        //
        //        )
        //    }
        //}
$(document).ready(function(){

    $(document.body).on("click", ".login", function(e){
     e.preventDefault();
     $("#loginModal").modal({})

});

    $(document.body).on("click", ".register", function(e){
     e.preventDefault();
     $("#registerModal").modal({})

});

    $(document.body).on("click", ".share-btn", function(e){
     e.preventDefault();
     $("#shareModal").modal({})
     $("#shareModal").on("shown.bs.modal", function(){
         $('.sharetext').focus()
     })

});

    $(document.body).on("click", ".playlist-btn", function(e){
     e.preventDefault();
     $("#playlistModal").modal({})

});

    $(document.body).on("click", ".delete-vid-btn", function(e){
     e.preventDefault();
     $("#deleteVideoModal").modal({})

});

    $(document.body).on("click", ".videoedit", function(e){
     e.preventDefault();
     $("#videoEditModal").modal({})

});

    $(document.body).on("click", ".playlistedit", function(e){
     e.preventDefault();
     $("#playlistEditModal").modal({})

});



      $(document.body).on("click", ".follow-btn", function(e){

      e.preventDefault()
      var this_ = $(this)
      var profileId = this_.attr("data-id")
      var followedUrl = '/api/accounts/' + profileId + '/follow/'

      // this_.text("Liked")
      $.ajax({
        method:"GET",
        url: followedUrl,
        success: function(data){
          if (data.following){
            this_.text("Unfollow " + data.follower_count)
            this_.css("color", "black")
            this_.addClass("btn btn-primary")
            //this_.mouseover(function(){
            //    this_.css("color", "white")
            //})

          } else {
            this_.text("Follow " + data.follower_count)
            this_.css("color", "black")
            this_.addClass("btn btn-primary")
            //this_.mouseover(function(){
            //    this_.css("color", "white")
            //})
          }
        },
        error: function(data){
            popUpLoginModal()
          console.log("error")
          console.log(data)
        }
      })
  })


      $(document.body).on("click", ".like-btn", function(e){
      e.preventDefault()
      var this_ = $(this)
      var videoId = this_.attr("data-id")
      var likedUrl = '/api/videos/' + videoId + "/like/"
      // this_.text("Liked")
      $.ajax({
        method:"GET",
        url: likedUrl,
        success: function(data){
          if (data.liked){
            this_.text("Unlike " + data.likes_count)
            this_.css("color", "black")
            this_.addClass("inline btn btn-primary commentbtn")
          } else {
            this_.text("Like " + data.likes_count)
            this_.css("color", "black")
            this_.addClass("inline btn btn-primary commentbtn")
          }
        },
        error: function(data){
          console.log("error")
          console.log(data)
          popUpLoginModal()
        }
      })
  })


      $(document.body).on("click", ".cmt-like-btn", function(e){
      e.preventDefault()
      var this_ = $(this)
      var commentId = this_.attr("data-id")
      var likedUrl = '/api/videos/comment/' + commentId + "/like/"
      // this_.text("Liked")
      $.ajax({
        method:"GET",
        url: likedUrl,
        success: function(data){
          if (data.liked){
            this_.text("Unlike " + data.likes_count)
            this_.css("color", "black")
            this_.addClass("inline btn btn-primary commentbtn")
          } else {
            this_.text("Like " + data.likes_count)
            this_.css("color", "black")
            this_.addClass("inline btn btn-primary commentbtn")
          }
        },
        error: function(data){
          console.log("error")
          console.log(data)
          popUpLoginModal()
        }
      })
  })

      $(document.body).on("click", ".deletecmt-btn", function(e){
      e.preventDefault()
      var this_ = $(this)
      var commentId = this_.attr("data-id")
      var deleteVideoUrl = '/api/videos/comment/' + commentId  + '/'
        swal({
        title: "Are you sure?",
        text: "Are you sure that you want to remove this comment?",
        type: "warning",
        showCancelButton: true,
        allowOutsideClick: true,
        closeOnConfirm: true,
        confirmButtonText: "Yes, delete it!",
        confirmButtonColor: "black"

    },
            function() {
                // this_.text("Liked")
                $.ajax({
                    method: "DELETE",
                    url: deleteVideoUrl,
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                    },
                    success: function (data) {
                        console.log("deleted")
                        $('#' + commentId).hide(500)
                    },
                    error: function (data) {
                        cannot()
                        console.log("error")
                        console.log(data)
                    }
                })
            })
  })






});

function cannot() {
    swal({title:"You Cannot Perform This Action",
          confirmButtonColor:"black",
          allowOutsideClick:"true"})
    }

function popUpLoginModal() {
        $("#loginModal").modal({})
    }

function popUpRegisterModal() {
        $("#registerModal").modal({})
    }

function preventModalClose() {
    $(document.body).on("click", "#regsubmit", function (e) {
        e.preventDefault();
        // $("#registerModal").modal({"backdrop": "static"});
        //$('body').fadeOut(3000)
    })
}


  function updateHashLinks() {
      $(".hash").each(function (data) {
          var hashtagRegex = /(^|\s)#([\w\d-]+)/g
          var newText = $(this).html().replace(hashtagRegex, "$1<a href='/tags/$2/'>#$2</a>")
          $(this).html(newText)

      })
  }




$(document).ready(function() {
    var showChar = 200;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "Show more &#9660";
    var lesstext = "Show less &#9650;";


    $('.more').each(function () {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<h5 class="morelink btn btn-primary">' + moretext + ' </h5></span>';
            $(this).html(html);

        }
            updateHashLinks()
    });

    $(".morelink").click(function () {
        if ($(this).hasClass("less")) {
            $(this).removeClass("less");

            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();

        return false;
    });
//    window.onscroll = function(ev) {
//    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
//        alert("you're at the bottom of the page");
//    }
//};
    //Selectors


    $('.fadeaway').fadeOut(1000)
});