function OpenDataShowCard()
{   
    $("data_select_control_label").className = "nav-link"
    $("data_analysis_control_label").className = "nav-link"
    $("data_predict_control_label").className = "nav-link"

    if ($("data_show_control_label").className == "nav-link")
    {
        $("data_show_control_label").className = "nav-link active"
        $("data_show_control_card").style.display = "block"    
    }
    else
    {
        $("data_show_control_label").className = "nav-link"
        $("data_show_control_card").style.display = "none"
        
    }

    alert("show")
}

function DataShow()
{
    url = location.href;
    $.ajax({
            url:url,
            type: 'POST',
            data: JSON.stringify({
                type: 'login',
                name: name,
                password: password,
            }),
            heads : {
                'content-type' : 'application/json;charset=UTF-8'
            },
            dataType: 'json',
            success: function(response, status) {
                // response {status,error_text/url}
                if (response.status == true) {
                    alert("登录成功！！")
                    location.href = response.url;
                } else {
                    alert(response.error_text);
                    password = ""
                }
            },
            error: function(request, textStatus, errorThrown) {
                alert("传送错误，请重试！！ 错误信息为: " + errorThrown )
            }
        });
}

function OpenDataSelectCard()
{
    $("data_show_control_label").className = "nav-link"
    $("data_select_control_label").className = "nav-link active"
    $("data_analysis_control_label").className = "nav-link"
    $("data_predict_control_label").className = "nav-link"

    $("data_show_control_card").style.display = "none"
    alert("select")
}

function OpenDataAnalysisCard()
{
    $("data_show_control_label").className = "nav-link"
    $("data_select_control_label").className = "nav-link"
    $("data_analysis_control_label").className = "nav-link active"
    $("data_predict_control_label").className = "nav-link"

    $("data_show_control_card").style.display = "none"
    alert("analysis")
}

function OpenDataPredictCard()
{
    $("data_show_control_label").className = "nav-link"
    $("data_select_control_label").className = "nav-link"
    $("data_analysis_control_label").className = "nav-link"
    $("data_predict_control_label").className = "nav-link active"

    $("data_show_control_card").style.display = "none"
    alert("predict")
}