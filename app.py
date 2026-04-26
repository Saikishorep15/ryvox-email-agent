from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from environment import RyvoxEmailEnvironment

app = FastAPI()
env = RyvoxEmailEnvironment()


class Action(BaseModel):
    action: str


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation":{
            "email_text":obs.email_text,
            "reward":obs.reward,
            "done":obs.done
        }
    }


@app.post("/step")
def step(action: Action):

    obs,reward,done,_=env.step(action)

    return {
        "observation":{
            "email_text":obs.email_text,
            "reward":obs.reward,
            "done":obs.done
        },
        "reward":reward,
        "done":done
    }


# ---------------- FRONTEND UI ---------------- #

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Ryvox AI Email Copilot</title>

<style>

body{
font-family:Arial;
background:#0f172a;
color:white;
text-align:center;
padding:40px;
}

.container{
max-width:850px;
margin:auto;
background:#1e293b;
padding:35px;
border-radius:20px;
box-shadow:0 0 20px rgba(0,0,0,.3);
}

h1{
font-size:42px;
color:#60a5fa;
}

textarea{
width:90%;
height:180px;
padding:20px;
font-size:18px;
border-radius:15px;
border:none;
margin-top:20px;
}

button{
padding:15px 30px;
margin:15px;
font-size:18px;
border:none;
border-radius:12px;
cursor:pointer;
background:#2563eb;
color:white;
}

button:hover{
background:#1d4ed8;
}

.card{
margin-top:25px;
background:#334155;
padding:25px;
border-radius:15px;
}

.result{
font-size:28px;
margin-top:20px;
font-weight:bold;
color:#34d399;
}

.badge{
display:inline-block;
padding:8px 18px;
background:#ef4444;
border-radius:30px;
margin-top:10px;
}

</style>
</head>

<body>

<div class="container">

<h1>📧 Ryvox AI Email Copilot</h1>

<p>
Spam Detection • Priority Detection • Smart Classification
</p>

<textarea id="emailBox">
Win $1000 now! Limited time offer.
</textarea>

<br>

<button onclick="loadTask()">
Load Email
</button>

<button onclick="checkSpam('spam')">
Mark Spam
</button>

<button onclick="checkSpam('important')">
Important
</button>

<button onclick="checkSpam('normal')">
Normal
</button>


<div class="card">
<h2>Email</h2>

<p id="emailText">
Press Load Email
</p>
</div>


<div class="card">
<h2>Prediction Result</h2>

<div id="prediction" class="result">
Waiting...
</div>

<div id="reward"></div>
</div>

</div>


<script>

async function loadTask(){

let r=await fetch('/reset',{
method:'POST'
});

let data=await r.json();

document.getElementById(
'emailText'
).innerHTML=
data.observation.email_text;

}


async function checkSpam(label){

let r=await fetch('/step',{

method:'POST',

headers:{
'Content-Type':'application/json'
},

body:JSON.stringify({
action:label
})

});

let data=await r.json();

document.getElementById(
'prediction'
).innerHTML=
"Reward: "+
data.reward;

document.getElementById(
'reward'
).innerHTML=
data.done ?
"<div class='badge'>Task Completed</div>"
:"Running";

}

</script>

</body>
</html>
"""


def main():
    return app


if __name__=="__main__":
    main()