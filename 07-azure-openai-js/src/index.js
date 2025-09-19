import 'dotenv/config';
import { AzureOpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const credential = new DefaultAzureCredential();
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);

const client = new AzureOpenAI({
  endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  azureADTokenProvider,
  deployment: process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
  apiVersion: process.env.AZURE_OPENAI_API_VERSION,
});

async function main() {
    const response = await client.responses.create({
        model: process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
        input: "Write a one-sentence bedtime story about a unicorn."
    });

    console.log(response.output_text);
}

main();