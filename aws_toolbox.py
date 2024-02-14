import argparse
import boto3
import aws_lambda_powertools
from moto import mock_aws


class aws_toolbox:
    def __init__(self,profile,region) -> None:
        self.session = boto3.session.Session(profile_name=profile,region_name=region)
        self.profile = profile
        self.region = region
    
    def main(self,command_line=None):
        """_summary_

        Args:
            commandline (_type_, optional): _description_. Defaults to None.
        """
        
        #Initiate the parser
        parser = argparse.ArgumentParser(
        prog="AWS ToolBox",
        description="Runs various basic functions against AWS to confirm access and permissions"        
        )
        subparsers = parser.add_subparsers(dest='service')

        acm = subparsers.add_parser("acm",help="AWS Certificate Manager")
        acmpca = subparsers.add_parser("acmpca",help="AWS Certificate Manager Private Certificate Authority")
        amp = subparsers.add_parser("amp",help="Amazon Managed Service for Prometheus")
        cloudfront = subparsers.add_parser("cloudfront")
        dynamo = subparsers.add_parser("dynamo")
        
        # dynamo.add_argument()
        lamb = subparsers.add_parser("lambda")
        
        
        
        args = parser.parse_args(command_line)
       
        if args.service == 'acm':
            self._acm()
        elif args.service == 'acmpca':
            self._acmpca()
        elif args.service == 'amp':
            self._amp()
        elif args.service == "dynamo":
            self._dynamo()
        elif args.service == "lambda":
            self._lambda()
        elif args.service == "cloudfront":
            self._cloudfront()
            
    def _acm(self):
        acm_client = self.session.client('acm')
        
        print("Executing AWS Certificate Manager")
        
        try:
            response = acm_client.list_certificates()
            print(f"List of Certificates: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")
        
        try:
            response = acm_client.get_account_configuration()
            print(f"Account Configuration: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")

    def _acmpca(self):
        acm_client = self.session.client('acm-pca')
        
        print("Executing AWS Certificate Manager Private Certificate Authority")
        
        try:
            response = acm_client.list_certificate_authorities()
            print(f"List of Certificates: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")

    def _amp(self):
        prom_client = self.session.client('amp')
        
        print("Executing Amazon Managed Service for Prometheus")
        
        try:
            response = prom_client.list_scrapers()
            print(f"List of Scrapers: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")

        try:
            response = prom_client.list_workspaces()
            print(f"List of Workspaces: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")

    def _dynamo(self):
        """_summary_
        """
        print("Executing Dynamo")
        dynamodb_client = self.session.client('dynamodb')
        
        try:
            print("List of Tables")
            response = dynamodb_client.list_tables()
            for table in response["TableNames"]:
                print(f"Table Name: {table}")
        except Exception as e:
            raise(f"Error occurred: {e}")
        
    def _lambda(self):
        """_summary_
        """
        print("Executing Lambda")
        lambda_client =self.session.client('lambda')
        
        try:
            print("Retrieiving list of Lambda Functions for Profile: {self.profile}")
            response = lambda_client.list_functions()
            for function in response["Functions"]:
                print(f"Function Name: {function["FunctionName"]}")
        except Exception as e:
            raise(f"Error occurred: {e}")
        
        
    def _cloudfront(self):
        """_summary_
        """
        print("Executing Cloud Front")
        cf_client =self.session.client('cloudfront')

        try:
            print("Retrieiving Functions")
            response = cf_client.list_functions()
            if response["FunctionList"]["Quantity"] >= 1:
                print(f"List of Cloud Front Functions: {response}")
            else:
                print("No Functions exist in this Profile")
        except Exception as e:
            raise(f"Error occurred: {e}")
        
        try:
            print("Retrieving Distributions")
            response = cf_client.list_distributions()
            print(f"List of CloudFront Distributions: {response}")
        except Exception as e:
            raise(f"Error occurred: {e}")

if __name__ == "__main__":

    profile_name = 'yellowfish-dev-admin'
    region = 'us-east-1'
    at = aws_toolbox(profile_name,region)
    at.main()