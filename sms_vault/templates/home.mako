<%inherit file="base.mako"/>

<%def name="title()">
SMS Vault - SMS Backup Manager
</%def>

<%def name="header()">
  ${self.main_menu()}
</%def>

<%def name="extra_head()">
<style>
  /*pre {
    background: inherit;
    border: none;
    display: inline;
  }*/
  p.msg {
    background: inherit;
    border: none;
    display: inline;
    white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
  }
</style>
<script type="application/x-javascript">

function update_msg_counts(response) {
  var msg_counts = JSON.parse(response);
  
  content = '';
  for(var idx in msg_counts){
    var item = msg_counts[idx];
    
    item_str = ' \
      <button class="btn btn-sm btn-primary" onclick="javascript:">' + item[0] + \
        ' <span class="badge"> (' + item[1] + ') </span></button>';
    //console.log(li_str);
    content += item_str;
  }
  
  return content;
}

function load_messages(contact_name){
  require(["dojo/dom", "dojo/request"],
    function(dom, request){
      target = dom.byId("conversation_heading");
      target.innerHTML = 'Fetching conversations for <b>' + contact_name + '</b> ....';
      
      request.get("/" + contact_name + "/messages").then(
          function(response){
              // Display the text file content
              //console.log(response);
              var messages = JSON.parse(response);
              var icon_class = '';
              var cell_number = '';
              //console.log(messages);
              content = '';
              for(var msg in messages){
                msg = messages[msg];
                //console.log(msg);
                if (msg['incoming']){
                  icon_class = "glyphicon glyphicon-chevron-left";
                  cell_number = msg["msg_from"];
                }else{
                  icon_class = "glyphicon glyphicon-chevron-right";
                  cell_number = msg["msg_to"];
                }
                
                msg_str = ' \
                <p> \
                  <span class="label label-default"> \
                    <span class="' + icon_class + '" aria-hidden="true"></span> (' + cell_number + ') ' + msg["timestamp"] + \
                    '</span> <p class="msg">' + msg['message'] + '</p></span> \
                </p>';
                    
                //console.log(msg_str);
                content += msg_str;
              }
              target = dom.byId("conversation");
              target.innerHTML = content;
              
              target = dom.byId("conversation_heading");
            target.innerHTML = 'Displaying conversations for <b>' + contact_name + '</b>';
          },
          function(error){
              // Display the error returned
              target.innerHTML = "<div class=\"error\">"+error+"<div>";
          }
        );
      
      var extra_target = dom.byId("contact_extra_options");
        
      request.get("/msg_count/year/" + contact_name).then(
        function(response){
            extra_target.innerHTML = update_msg_counts(response);
        },
        function(error){
            // Display the error returned
            extra_target.innerHTML = "<div class=\"error\">"+error+"<div>";
        }
      );
  });
  
}

require(["dojo/dom", "dojo/request", "dojo/domReady!"],
    function(dom, request){
        
        var target = dom.byId("contacts");
        
        request.get("${request.route_url('msg_counts')}").then(
          function(response){
              var msg_counts = JSON.parse(response);
              
              content = '';
              for(var idx in msg_counts){
                msg_count = msg_counts[idx];
                var total_msgs = parseInt(msg_count['incoming'])+parseInt(msg_count['outgoing']);
                
                li_str = ' \
                <li role="presentation"> \
                  <a href="javascript:load_messages(\'' + msg_count['contact_name'] + '\');">' + msg_count['contact_name'] + ' \
                    <span class="badge"> \
                      <span class="glyphicon glyphicon-resize-small" aria-hidden="true"></span>' + \
                      total_msgs + \
                    '</span> \
                    <span class="badge"> \
                      <span class="glyphicon glyphicon-log-in" aria-hidden="true"></span>' + \
                      msg_count['incoming'] + \
                    '</span> \
                    <span class="badge"> \
                      <span class="glyphicon glyphicon-new-window" aria-hidden="true"></span>' + \
                      msg_count['outgoing'] + \
                    '</span> \
                  </a> \
                </li>';
                //console.log(li_str);
                content += li_str;
              }   
              target.innerHTML = content;
          },
          function(error){
              // Display the error returned
              target.innerHTML = "<div class=\"error\">"+error+"<div>";
          }
        );
        
        var extra_target = dom.byId("extra_options");
        
        request.get("/msg_count/year").then(
          function(response){
              extra_target.innerHTML = update_msg_counts(response);
          },
          function(error){
              // Display the error returned
              extra_target.innerHTML = "<div class=\"error\">"+error+"<div>";
          }
        );
    }
);
</script>
</%def>
  
  <div class="row" >
    <div class="panel panel-default col-md-6 col-lg-4 hidden-sm hidden-xs">
      <div class="panel-body">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="Search ...">
          <span class="input-group-btn">
            <button class="btn btn-primary" type="button">Search</button>
          </span>
        </div>
        <br />
        <div id="extra_options">Extra options come here</div>
        
      </div>
      
      <div style="overflow-y: auto; height: 470px;">
        <ul id="contacts" class="nav nav-pills nav-stacked">
        </ul>
      </div>
    </div>
    <div class="panel panel-primary col-md-6 col-lg-8 col-sm-12 col-xs-12">
      <div id="conversation_heading" class="panel-heading">Please select a contact to view it's conversation</div>
      <div class="panel-body">
        <div id="contact_extra_options">Extra options come here</div>
        <div style="overflow-y: auto; height: 490px;">
          <div id="conversation">
            
          </div>
        </div>
      </div>
    </div>
  </div>  
