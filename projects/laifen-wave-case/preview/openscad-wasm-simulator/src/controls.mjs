/** Bind a range control without allowing its browser coercion to own draft state. */
export function bindRange({input,range,onChange,onFocus}) {
  range.addEventListener('input',()=>{const value=range.value;if(onChange(value)!==false)input.value=value;});
  range.addEventListener('focus',onFocus);
}
