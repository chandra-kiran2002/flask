withCredentials([usernamePassword(credentialsId: 'dockerhub-user',
                                 usernameVariable: 'USER',
                                 passwordVariable: 'PASS')]) {
    sh "echo $PASS | docker login -u $USER --password-stdin"
}
