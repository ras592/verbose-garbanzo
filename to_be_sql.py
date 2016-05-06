to_be_implemented_sql = [
	"""
	'INSERT INTO local_sl.representative VALUES(
		{0}, "{1}", "{2}", "{3}", {4}, {5}, {6}
	)'.format(values['rep_no'], values['name'], values['address'], values['phone'], values['base_salary'], values['ytd_sales'], values['comm'])
	""",
	"""
	'INSERT INTO local_kc.sales_person VALUES(
		{0}, "{1}", "{2}", "{3}", {4}, {5}, {6}
	)'.format(values['sale_no'], values['name'], values['address'], values['phone'], values['comm'], values['base_salary'], values['ytdsales'])
	""",
	"""
	'INSERT INTO global.employee VALUES(
		{0}, "{1}", "{2}", "{3}", "{4}"
	)'.format(values['emp_no'], values['name'], values['address'], values['phone'], values['position'])
	""",
	"""
	'INSERT INTO global.salesperson VALUES(
		{0}, {1}, {2}, {3}
	)'.format(values['rep_no'], values['base_salary'], values['ytd_sales'], values['comm'])
	""",
	"""
	'INSERT INTO local_kc.finance VALUES(
		{0}, {1}, {2}, {3}, {4}
	)'.format(values['vehicle_no'], values['buyer_no'], values['amount'], values['months'], values['balance'])
	""",
	"""
	SELECT *
	FROM local_sl.representative
	""",
	"""
	SELECT *
	FROM local_kc.sales_person
	""",
	"""
	SELECT *
	FROM global.salesperson
	""",
	"""
	SELECT *
	FROM global.employee
	""",
	"""
	SELECT COUNT(*) 
	FROM local_sl.representative
	""",
	"""
	SELECT COUNT(*) 
	FROM local_kc.sales_person
	""",
	"""
	SELECT COUNT(*) 
	FROM local_sl.customer_d1
	""",
	"""
	SELECT COUNT(*) 
	FROM local_kc.customer_d2
	""",
	"""
	SELECT * 
	FROM local_sl.loan
	ORDER BY amount DESC LIMIT 1
	""",
	"""
	SELECT customer_d1.customer_no, customer_d1.name, customer_d1.address, customer_d1.phone, customer_d1.email 
	FROM local_sl.customer_d1, local_sl.loan
	WHERE customer_d1.customer_no = loan.customer_no
	""",
	"""
	SELECT * 
	FROM local_kc.finance
	ORDER BY amount DESC LIMIT 1
	""",
	"""
	SELECT customer_d2.buyer_no, customer_d2.name, customer_d2.address, customer_d2.phone, customer_d2.email 
	FROM local_kc.customer_d2, local_kc.finance
	WHERE customer_d2.buyer_no = finance.buyer_no
	""",
	"""
	SELECT autos.vehicle_no, autos.model, autos.color, autos.autotrans, autos.warehouse, autos.financed, finance.amount
	FROM local_kc.autos, local_kc.finance
	WHERE finance.vehicle_no = autos.vehicle_no
	ORDER BY finance.amount DESC LIMIT 1
	""",
	"""
	SELECT cars.serial_no, cars.model, cars.color, cars.autotrans, cars.warehouse, loan.amount
	FROM local_sl.cars, local_sl.loan
	WHERE loan.serial_no = cars.serial_no
	ORDER BY loan.amount DESC LIMIT 1
	""",
	"""
	SELECT *
	FROM global.salesperson
	ORDER BY comm DESC LIMIT 1
	""",
	"""
	SELECT available_auto.serial_no, available_auto.model, available_auto.color, available_auto.dealer, model.price 
	FROM global.available_auto, global.model 
	WHERE model.model = available_auto.model 
	ORDER BY model.price DESC
	""",
	"""
	SELECT available_auto.serial_no, available_auto.model, available_auto.color, available_auto.dealer, model.gas_mileage 
	FROM global.available_auto, global.model 
	WHERE model.model = available_auto.model 
	ORDER BY model.gas_mileage DESC
	""",
	"""
	SELECT available_auto.serial_no, available_auto.model, available_auto.color, available_auto.dealer, model.engine 
	FROM global.available_auto, global.model 
	WHERE model.model = available_auto.model 
	ORDER BY model.engine DESC
	"""
]