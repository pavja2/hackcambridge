periodicTable = {'Ru': 'rhodium', 'Pd': 'palladium', 'Pt': 'platinum', 'Ni': 'nickel', 'Mg': 'magnesium', 'Na': 'sodium', 'Nb': 'niobium', 'Db': 'dubnium', 'Ne': 'neon', 'Li': 'lithium', 'Pb': 'lead', 'Re': 'rhenium', 'Tl': 'thallium', 'B': 'boron', 'Ra': 'radium', 'Rb': 'rubidium', 'Ti': 'titanium', 'Rn': 'radon', 'Cd': 'cadmium', 'Po': 'polonium', 'Ta': 'tantalum', 'Be': 'beryllium', 'Fr': 'francium', 'Te': 'tellerium', 'Ba': 'barium', 'Os': 'osmium', 'La': 'lanthanum', 'Bh': 'bohrium', 'Ge': 'germanium', 'Zr': 'zirconium', 'Tc': 'technetium', 'Fe': 'iron', 'Br': 'bromine', 'Sr': 'strontium', 'Hf': 'hafnium', 'Hg': 'mercury', 'He': 'helium', 'C': 'carbon', 'Cl': 'chlorine', 'Rf': 'rutherfordium', 'P': 'phosphorus', 'F': 'fluorine', 'I': 'iodine', 'H': 'hydrogen', 'Mo': 'molybdenum', 'v': 'vanadium', 'Ac': 'actinium', 'O': 'oxygen', 'N': 'nitrogen', 'Kr': 'krypton', 'Si': 'silicon', 'Sn': 'tin', 'W': 'tungsten', 'Y': 'yttrium', 'Sb': 'antimony', 'Bi': 'bismuth', 'Al': 'aluminum', 'Sg': 'seaborgium', 'Se': 'selenium', 'Sc': 'scandium', 'Zn': 'zinc', 'Co': 'cobalt', 'Ag': 'silver', 'Mt': 'meitnerium', 'k': 'potassium', 'Ir': 'iridium', 'S': 'sulfur', 'Xe': 'xenon', 'Mn': 'manganese', 'As': 'arsenic', 'Ar': 'argon', 'Au': 'gold', 'At': 'astatine', 'Ga': 'gallium', 'Hs': 'hassium', 'Cs': 'cesium', 'Cr': 'chromium', 'Ca': 'calcium', 'Cu': 'copper', 'In': 'indium'}

returnArray = []

def ChemRec(text):
	textArray = text.split()
	for word in textArray:
		for key in periodicTable:
			if word.find(key) >= 0 and len(word) == len(key):
				returnArray.append(periodicTable[key])
	
	print returnArray	
	return returnArray 

ChemRec("Na Cu N is trOalala")
