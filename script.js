const screen = document.querySelector('#screen');
let current = '';
let pending = null;
let op = null;
let activeOpBtn = null;

const update = (value) => screen.textContent = value || '0';
const clearActiveOp = () => { if (activeOpBtn) { activeOpBtn.classList.remove('active'); activeOpBtn = null; } };
const setActiveOp = (action) => {
  clearActiveOp();
  activeOpBtn = document.querySelector(`.btn.op[data-action="${action}"]`);
  if (activeOpBtn) activeOpBtn.classList.add('active');
};
const reset = () => { current = ''; pending = null; op = null; clearActiveOp(); update('0'); };

const mapOp = { add: (a,b)=>a+b, subtract:(a,b)=>a-b, multiply:(a,b)=>a*b, divide:(a,b)=>b===0?null:a/b };

const calculate = () => {
  const a = parseFloat(pending);
  const b = parseFloat(current);
  if (isNaN(a)||isNaN(b)||!op) return;
  const r = mapOp[op](a,b);
  if (r===null) { reset(); update('Error'); return; }
  current = String(parseFloat(r.toPrecision(12))).replace(/\.0+$/, '');
  pending = null; op = null; clearActiveOp(); update(current);
};

const append = (c) => {
  if (c==='.' && current.includes('.')) return;
  if (current.length>=16) return;
  current = current==='0' && c !== '.' ? c : current + c;
  update(current);
};

const applyOp = (action) => {
  if (!current && pending) { op = action; setActiveOp(action); return; }
  if (!current) return;
  if (pending) calculate();
  op = action;
  pending = current;
  current = '';
  setActiveOp(action);
};

const actions = {
  clear: reset,
  negate: () => { if (!current) return; current = current.startsWith('-') ? current.slice(1) : '-' + current; update(current); },
  percent: () => { if (!current) return; current = String(parseFloat(current) / 100); update(current); },
  equal: calculate
};

const keyMap = {
  '+':'add', '-':'subtract', '*':'multiply', '/':'divide',
  'Add':'add', 'Subtract':'subtract', 'Multiply':'multiply', 'Divide':'divide'
};

const click = (e) => {
  const d = e.target.dataset.digit;
  const a = e.target.dataset.action;
  if (d !== undefined) return append(d);
  if (actions[a]) return actions[a]();
  if (['add','subtract','multiply','divide'].includes(a)) return applyOp(a);
};

const keydown = (e) => {
  const key = e.key;
  if (/^[0-9.]$/.test(key)) return append(key);
  if (key === 'Escape') return reset();
  if (key === 'Enter' || key === 'NumpadEnter') {
    e.preventDefault();
    return calculate();
  }
  if (key === '=') return calculate();
  if (keyMap[key]) return applyOp(keyMap[key]);
};

document.querySelectorAll('.btn').forEach(b => b.addEventListener('click', click));
window.addEventListener('keydown', keydown);
reset();
