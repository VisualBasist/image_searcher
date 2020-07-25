const IMAGE_LIMIT_COUNT=500;
const SERVER_PORT=55000;

function is_Enter(e){
    //TODO:codeとkeyどっちがいいかな?
    return e.code=="Enter";
}

function html_escape(s){
    const escape_map={"&": "&amp;","<": "&lt;",">": "&gt;"};
    return s.replace(/[&<>]/g,(x)=>{return escape_map[x]});
}

function fetch_images(){
    const xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    xhr.open("GET", `http://localhost:${SERVER_PORT}/images?sql=${encodeURIComponent(document.getElementById("sql").value)}`);
    xhr.onload=()=>{
        document.getElementById("message").innerText="";
        const image_list=document.getElementById("image_list");
        if(xhr.status=="400"){
            document.getElementById("message").innerText=xhr.response;
            return;
        }
        if(xhr.response.length>IMAGE_LIMIT_COUNT){
            document.getElementById("message").innerText=`${IMAGE_LIMIT_COUNT}件越えは省略したぞう`;
        }
        document.getElementById("search_time").innerText=`🐘「${xhr.response.length}件 ${(new Date()-start_date)/1e3}秒でみつけたぞう」`;
        image_list.innerHTML="";
        for(const image of xhr.response.slice(0,IMAGE_LIMIT_COUNT)){
            image_list.insertAdjacentHTML("beforeend",
`<div>
    <div>${image.author_name}</div>
    <div>
        <a href="${image.url}" target="_blank">
            <div>${image.name}</div>
        </a>
    </div>
    <div>
        <a href="file:///${image.path}" target="_blank">
            <img src="file:///${image.path}">
        </a>
    </div>
    <div class="tags">${image.tags.join(",")}</div>
    <button data-id="${image.id}" onclick="add_tag(event)">タグ追加</button>
</div>`);
        }
    };
    const start_date=new Date();
    xhr.send();
}

function add_tag(e){
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `http://localhost:${SERVER_PORT}/add_tag`);
    xhr.onload = ()=>{
        fetch_images();
    };
    const tag=document.getElementById("tag").value;
    if(tag==""){
        return;
    }
    xhr.send(JSON.stringify({id:e.target.dataset.id,tag:tag}));
}
