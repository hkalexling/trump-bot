const predict = (str, cb) => {
	$.get('/predict', {
			input: str
		})
		.then(data => {
			cb(data.new_word);
		})
		.catch(e => {
			console.error(e);
		});
};

/**
 * Set an alpine.js property
 *
 * @function setProp
 * @param {string} key - Key of the data property
 * @param {*} prop - The data property
 */
const setProp = (key, prop) => {
	$('#root').get(0).__x.$data[key] = prop;
};

/**
 * Get an alpine.js property
 *
 * @function getProp
 * @param {string} key - Key of the data property
 * @return {*} The data property
 */
const getProp = (key) => {
	return $('#root').get(0).__x.$data[key];
};


const update = () => {
	const updating = getProp('updating');
	if (updating) return;

	setProp('submitted', true);

	let text = getProp('text').trim();
	text = text.charAt(0).toUpperCase() + text.slice(1);

	predict(text, newWord => {
		setProp('updating', false);
		setProp('text', text + ' ' + newWord);
	});
};
