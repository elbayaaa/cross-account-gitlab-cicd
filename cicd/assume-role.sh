USER_AWS_ACCESS_KEY_ID=$1
USER_AWS_SECRET_ACCESS_KEY=$2
REGION=$3
ROLE=$4
SESSION_NAME=$5

# unassume currently assumed role, if any.
if [ "$AWS_ACCESS_KEY_ID" != "$USER_AWS_ACCESS_KEY_ID" ]
then
  unset AWS_SESSION_TOKEN
  export AWS_ACCESS_KEY_ID=$USER_AWS_ACCESS_KEY_ID
  export AWS_SECRET_ACCESS_KEY=$USER_AWS_SECRET_ACCESS_KEY
fi

cred=$(aws sts assume-role \
           --role-arn $ROLE \
           --role-session-name $SESSION_NAME)

export AWS_DEFAULT_REGION=$REGION
export AWS_ACCESS_KEY_ID=$(echo "${cred}" | jq ".Credentials.AccessKeyId" --raw-output)
export AWS_SECRET_ACCESS_KEY=$(echo "${cred}" | jq ".Credentials.SecretAccessKey" --raw-output)
export AWS_SESSION_TOKEN=$(echo "${cred}" | jq ".Credentials.SessionToken" --raw-output)
