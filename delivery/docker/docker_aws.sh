rm results
mkdir results

docker build -f Dockerfile -t aut-test-delivery  ../
docker run -it --rm --name aut-test-delivery -v c6-automation-delivery:/results aut-test-delivery

echo 'The results of the execution are in '
docker volume inspect c6-automation-delivery