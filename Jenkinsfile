@Library('xmos_jenkins_shared_library@v0.20.0') _

getApproval()

pipeline {
    agent none
    options {
        disableConcurrentBuilds()
        skipDefaultCheckout()
        timestamps()
        // on develop discard builds after a certain number else keep forever
        buildDiscarder(logRotator(
            numToKeepStr:         env.BRANCH_NAME ==~ /develop/ ? '25' : '',
            artifactNumToKeepStr: env.BRANCH_NAME ==~ /develop/ ? '25' : ''
        ))
    }    
    parameters {
        string(
            name: 'TOOLS_VERSION',
            defaultValue: '15.2.1',
            description: 'The XTC tools version'
        )
    }    
    environment {
        PYTHON_VERSION = "3.8.11"
        VENV_DIRNAME = ".venv"
        BUILD_DIRNAME = "dist"
        RTOS_TEST_RIG_TARGET = "xcore_sdk_test_rig"
    }    
    stages {
        stage('Setup') {
            agent {
                label 'xcore.ai-explorer-us'
            }
            stages{
                stage('Checkout') {
                    steps {
                        checkout scm
                        sh 'git submodule update --init --recursive --depth 1 --jobs \$(nproc)'
                    }
                }
                stage('Build applications and firmware') {
                    steps {
                        script {
                            uid = sh(returnStdout: true, script: 'id -u').trim()
                            gid = sh(returnStdout: true, script: 'id -g').trim()
                        }
                        withTools(params.TOOLS_VERSION) {
                            // test applications and firmware
                            sh "bash tools/ci/build_rtos_tests.sh"
                        }
                        // List built files for log
                        sh "ls -la dist/"
                    }
                }
                stage('Create virtual environment') {
                    steps {
                        // Create venv
                        sh "pyenv install -s $PYTHON_VERSION"
                        sh "~/.pyenv/versions/$PYTHON_VERSION/bin/python -m venv $VENV_DIRNAME"
                        // Install dependencies
                        withVenv() {
                            sh "pip install git+https://github0.xmos.com/xmos-int/xtagctl.git"
                            sh "pip install -r test/requirements.txt"
                        }
                    }
                }
                stage('Cleanup xtagctl') {
                    steps {
                        // Cleanup any xtagctl cruft from previous failed runs
                        withTools(params.TOOLS_VERSION) {
                            withVenv {
                                sh "xtagctl reset_all $RTOS_TEST_RIG_TARGET"
                            }
                        }
                        sh "rm -f ~/.xtag/status.lock ~/.xtag/acquired"
                    }
                }
            }
        }
        stage('Standard tests') {
            agent {
                label 'xcore.ai-explorer-us'
            }
            stages{
                stage('Run RTOS Drivers HIL test') {
                    steps {
                        withTools(params.TOOLS_VERSION) {
                            withVenv {
                                script {
                                    withXTAG(["$RTOS_TEST_RIG_TARGET"]) { adapterIDs ->
                                        sh "test/rtos_drivers/hil/check_drivers_hil.sh " + adapterIDs[0]
                                    }
                                    sh "pytest test/rtos_drivers/hil"
                                }
                            }
                        }
                    }
                }
                stage('Run RTOS Drivers HIL_Add test') {
                    steps {
                        withTools(params.TOOLS_VERSION) {
                            withVenv {
                                script {
                                    withXTAG(["$RTOS_TEST_RIG_TARGET"]) { adapterIDs ->
                                        sh "test/rtos_drivers/hil_add/check_drivers_hil_add.sh " + adapterIDs[0]
                                    }
                                    sh "pytest test/rtos_drivers/hil_add"
                                }
                            }
                        }
                    }
                }
            }
            post {
                cleanup {
                    // cleanWs removes all output and artifacts of the Jenkins pipeline
                    //   Comment out this post section to leave the workspace which can be useful for running items on the Jenkins agent. 
                    //   However, beware that this pipeline will not run if the workspace is not manually cleaned.
                    cleanWs()
                }
            }
        }
    }
}
