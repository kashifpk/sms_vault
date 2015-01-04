<%inherit file="base.mako"/>

<%def name="title()">
SMS Vault - SMS Backup Manager
</%def>

<%def name="header()">
  ${self.main_menu()}
</%def>

<%def name="extra_head()">
<script type="application/x-javascript">
require(["dojo/dom", "dojo/on", "dojo/request", "dojo/domReady!"],
    function(dom, on, request){
        // Results will be displayed in resultDiv
        var resultDiv = dom.byId("contacts");
        
        request.get("${request.route_url('msg_counts')}").then(
              function(response){
                  // Display the text file content
                  //console.log(response);
                  var msg_counts = JSON.parse(response);
                  content = '';
                  for(var contact in msg_counts){
                    li_str = ' \
                    <li role="presentation"> \
                      <a href="javascript:">' + contact + ' \
                        <span class="badge"> \
                          <span class="glyphicon glyphicon-resize-small" aria-hidden="true"></span>' + \
                          msg_counts[contact]['incoming']+msg_counts[contact]['outgoing'] + \
                        '</span> \
                        <span class="badge"> \
                          <span class="glyphicon glyphicon-log-in" aria-hidden="true"></span>' + \
                          msg_counts[contact]['incoming'] + \
                        '</span> \
                        <span class="badge"> \
                          <span class="glyphicon glyphicon-new-window" aria-hidden="true"></span>' + \
                          msg_counts[contact]['outgoing'] + \
                        '</span> \
                      </a> \
                    </li>';
                    //console.log(li_str);
                    content += li_str;
                  }   
                  resultDiv.innerHTML = content;
              },
              function(error){
                  // Display the error returned
                  resultDiv.innerHTML = "<div class=\"error\">"+error+"<div>";
              }
          );
        
        
 
        // Attach the onclick event handler to the textButton
            
        
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
        
      </div>
      
      <div  style="overflow-y: auto; height: 500px;">
        <ul id="contacts" class="nav nav-pills nav-stacked">
        </ul>
      </div>
    </div>
  </div>  
