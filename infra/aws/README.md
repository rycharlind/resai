# ResAI AWS Cloudformation

The ResAI AWS stack with cloudformation.  

## Deploy

`aws cloudformation deploy --stack-name resai-stack --template-file resai-stack.yaml --capabilities CAPABILITY_NAMED_IAM`

```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"iam:GetRole",
				"iam:PassRole"
			],
			"Resource": "arn:aws:iam::408545242574:user/resai_service_dev"
		}
	]
}
```