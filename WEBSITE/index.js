const result = document.getElementById('result');
const form=document.querySelector('form')
form.addEventListener('submit',(e)=>{
  e.preventDefault();
  func();
})

async function func() {
  var url = document.querySelector('input').value;
  const response = await fetch(`http://127.0.0.1:5000/predict?url=${url}`);
  await response.json().then( (data) => {
    result.innerText = data.score;
    let score=data.score;
    if(score>85){
      result.classList.add('danger');
      result.classList.remove('good');
      result.classList.remove('average');
    
      result.classList.remove('medium');
    }
    else if(score<25) { result.classList.add('good')
    result.classList.remove('danger');
    result.classList.remove('average');
    result.classList.remove('medium');

  }
    else if (score>25 && score<50) { result.classList.add('average')
    result.classList.remove('danger');
    result.classList.remove('medium');
    result.classList.remove('good');


  }
    else if(score>51 && score<85) { result.classList.add('medium')
    result.classList.remove('danger');
    result.classList.remove('good');
    result.classList.remove('average');
  }

    
    console.log(data.score);
  });


}
 

document.getElementById("clear").addEventListener('click',() => {
  document.getElementById("url").value = '';
  result.innerHTML='';
  result.classList.remove('danger');
  result.classList.remove('good');
  result.classList.remove('average');

  result.classList.remove('medium');



})
