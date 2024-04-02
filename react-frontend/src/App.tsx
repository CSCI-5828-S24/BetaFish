import React, { useState } from 'react';
import './App.css';

type TGlobalState = {
  num1: number | null,
  num2: number | null,
  product: number | null
}

function App() {
  const [state, setState] = useState<TGlobalState>({
    num1: null,
    num2: null,
    product: null
  })


  const handleClick = () => {
    fetch(`${window.location.href}/api/multiply/${state.num1}/${state.num2}`)
      .then(response => response.json())
      .then(json => setState(prevState => {
        return {
          ...prevState,
          product: json["data"]
        }
      }))
      .catch(error => console.log(error));
  }

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setState(prevState => {
      return {
        ...prevState,
        [event.target.name]: event.target.value
      }
    })
  }

  return (
    <div className="App">
      <div className="MultiplySection">
        <p>Multiply:</p>
        <input onChange={handleChange} type='number' id="number1-inp" name="num1" value={state.num1 === null? "":state.num1 as number}/>
        <input onChange={handleChange} type='number' id="number2-inp" name="num2" value={state.num2 === null? "":state.num2 as number}/>
        <button onClick={handleClick}>Check</button>
        <p id="multiply-results">{state.product}</p>
      </div>
    </div>
  );
}

export default App;
