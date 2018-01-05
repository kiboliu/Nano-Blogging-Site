//sends a new request to update the posts list
function getList() {
    $.ajax({
        url: "/socialnetwork/get_post",
        dataType: "json",
        success: function(response) {
            updateList(response);
        },
        error: function(XHR, textStatus, errorThrown) {
            console.log('error' + errorThrown);
        }
    });
    console.log("get list!");
}
function updateList(posts) {
    console.log("update!")
    //removes the old list items
    $("#postlist").empty();
    var username = $("#loginusername");
    var profile = $("#profilefollows");
    console.log(profile.val());
    var id = 1;
    //add each new list items to the list
    $(posts).each(function() {
        console.log(this.fields.user);
        if(this.fields.user == username.val()) {
            $("#postlist").append(
                "<li class='collection-item avatar'><img src='/socialnetwork/photo/"+this.fields.user+"' class='circle'/>" +
                "<span class='title'>"+this.fields.user+"</span>" +
                "<p>"+this.fields.date+"<br/>"+sanitize(this.fields.content)+"</p><br/>" +
                "<a href='/socialnetwork/profile/"+this.fields.user+"' class='secondary-content'><i class='material-icons medium'>description</i></a>"+
                "</li>" +
                "<div class='row'><ul id='commentlist"+id+"' class='collection with-header'><li class='collection-header'><h6>Comments</h6></li></ul></div>" +
                "<div class='row'><input type='hidden' name='postid' id='post"+id+"' value='"+this.pk+"'/>" +
                    "<div class='input-field col s12'>"+
                        "<span id='error'></span>" +
                        "<input type='text' name='comment' id='comment"+id+"'/>"+
                        "<label for='comment'>Type new comment here...(maximum 100 chars)</label>"+
                        "<button class='btn waves-effect indigo' onclick='addComment("+id+")'>Add Comment<i class='material-icons right'>create</i></button>"+
                    "</div>"+
                "</div>"
            );
        } else if(profile.val() == [] || profile.val().indexOf(this.fields.user) < 0) {
            $("#postlist").append(
                "<li class='collection-item avatar'><img src='/socialnetwork/photo/"+this.fields.user+"' class='circle'/>" +
                "<span class='title'>"+this.fields.user+"</span>" +
                "<p>"+this.fields.date+"<br/>"+sanitize(this.fields.content)+"</p><br/>" +
                "<a href='/socialnetwork/follow/"+this.fields.user+"'><button class='btn red' type='submit'>Follow</button></a>" +
                "<a href='/socialnetwork/profile/"+this.fields.user+"' class='secondary-content'><i class='material-icons medium'>description</i></a>"+
                "</li>" +
                "<div class='row'><ul id='commentlist"+id+"' class='collection with-header'><li class='collection-header'><h6>Comments</h6></li></ul></div>" +
                "<div class='row'><input type='hidden' name='postid' id='post"+id+"' value='"+this.pk+"'/>" +
                    "<div class='input-field col s12'>"+
                        "<span id='error'></span>" +
                        "<input type='text' name='comment' id='comment"+id+"'/>"+
                        "<label for='comment'>Type new comment here...(maximum 100 chars)</label>"+
                        "<button class='btn waves-effect indigo' onclick='addComment("+id+")'>Add Comment<i class='material-icons right'>create</i></button>"+
                    "</div>"+
                "</div>"
            );
        } else {
            "<li class='collection-item avatar'><img src='/socialnetwork/photo/"+this.fields.user+"' class='circle'/>" +
            "<span class='title'>"+this.fields.user+"</span>" +
            "<p>"+this.fields.date+"<br/>"+sanitize(this.fields.content)+"</p><br/>" +
            "<a href='/socialnetwork/unfollow/"+this.fields.user+"'><button class='btn red' type='submit'>UnFollow</button></a>" +
            "<a href='/socialnetwork/profile/"+this.fields.user+"' class='secondary-content'><i class='material-icons medium'>description</i></a>"+
            "</li>" +
            "<div class='row'><ul id='commentlist"+id+"' class='collection with-header'><li class='collection-header'><h6>Comments</h6></li></ul></div>" +
            "<div class='row'><input type='hidden' name='postid' id='post"+id+"' value='"+this.pk+"'/>" +
                "<div class='input-field col s12'>"+
                    "<span id='error'></span>" +
                    "<input type='text' name='comment' id='comment"+id+"'/>"+
                    "<label for='comment'>Type new comment here...(maximum 100 chars)</label>"+
                    "<button class='btn waves-effect indigo' onclick='addComment("+id+")'>Add Comment<i class='material-icons right'>create</i></button>"+
                "</div>"+
            "</div>"
        }
        // $("#postlist").append(
        //     "<li class='collection-item avatar'><img src='/socialnetwork/photo/"+this.fields.user+"' class='circle'/>" +
        //     "<span class='title'>"+this.fields.user+"</span>" +
        //     "<p>"+this.fields.date+"<br/>"+sanitize(this.fields.content)+"</p><br/>" +
        //     "{% if "+this.fields.user+" == user %}" + 

        //     "{% elif"+this.fields.user.username+"not in profile.follows %}" +
        //     "<form method='post' action={% url"+' "follow" '+this.fields.user+" %}>" +
        //         "<button class='btn red' type='submit'>Follow</button>" +
        //         "{% csrf_token %}" +
        //     "</form>" +
        //     "{% else %}" +
        //     "<form method='post' action={% url"+' "unfollow" '+this.fields.user+" %}>" +
        //         "<button class='btn grey' type='submit'>UnFollow</button>" +
        //         "{% csrf_token %}" +
        //     "</form>" +
        //     "{% endif %}" +
        //     "<a href='{% url"+' "profile" '+this.fields.user+" %}' class='secondary-content'><i class='material-icons medium;>description</i></a>"+
        //     "</li>" +
        //     "<div class='row'><ul id='commentlist' class='collection'></ul></div>" +
        //     "<div class='row'><input type='hidden' name='postid' id='postid' value="+this.pk+"/><form class='col s12' method='post' action='{% url"+' "addcomment" '+" %}'>" +
        //         "<div class='input-field col s12'>"+
        //             "<span id='error'></span>" +
        //             "<input type='text' name='comment' id='comment'/>"+
        //             "<label for='comment'>Type new comment here...(maximum 100 chars)</label>"+
        //             "<button class='btn waves-effect indigo' onclick='addComment()'>Add Comment<i class='material-icons right'>create</i></button>"+
        //         "</div>{% csrf_token %}</form>"+
        //     "</div>"
        // );
        $(this.comments).each(function() {
            console.log("comments!");
            $("#commentlist"+id).append(
                "<li class='collection-item'><img src='/socialnetwork/photo/"+this.fields.user+"' class='circle' style='width:30px'/>"+"<span style='margin-left:2%'>"+this.fields.user+"</span><span style='margin-left:60%'>"+this.fields.time+"</span>" +
                "<p>"+this.fields.content+"</p></li>"
            );
        });
        id = id + 1;
    });
}

function sanitize(s) {
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].trim().startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length+1, cookies[i].length);
        }
    }
    return "unknown";
}
function addPost() {
    var postElement = $("#content");
    var postValue = postElement.val();
    postElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add_post",
        type: "POST",
        data: "content="+postValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}
function addComment(id) {
    console.log(id);
    var commentElement = $("#comment"+id);
    var postId = $("#post"+id);
    // var postId = $('[id="'+post+'"]');
    var commentValue = commentElement.val();
    console.log(commentValue)
    console.log(postId.val())
    commentElement.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add_comment",
        type: "POST",
        data: "comment="+commentValue+"&postid="+postId.val()+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

window.onload = getList;

// window.setInterval(getList, 5000);