USE customer_data
GO 
SELECT
	CAST(date AS date) AS date_only,
	purchase_price
FROM 
	[customer_data].[dbo].[customer_purchase]