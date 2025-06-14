// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7;

contract ModelStorage {

    // a Model struct : model, accuracy and author of the model

    string base_model_structure;

    struct Model {
        string ipfs_model;
        uint256 accuracy;
        address author;
    }

    Model[] models;

    // constructor will initialize a first random-weight model

    constructor(string memory ipfs_struct, string memory ipfs_weight, uint256 accuracy_) {
        base_model_structure = ipfs_struct;
        Model memory tmp = Model({
            ipfs_model: ipfs_weight,
            accuracy: accuracy_,
            author: msg.sender
        });
        models.push(tmp);
    }

    function submit_model_weight(string memory ipfs_, uint256 accuracy_) public {
        Model memory submit_ = Model({
            ipfs_model: ipfs_,
            accuracy: accuracy_,
            author: msg.sender
        });

        models.push(submit_);
    }

    function get_model() view public returns(string memory) {
        return base_model_structure;
    }

    function get_latest_model_weight() view public returns(string memory) {
        return models[models.length - 1].ipfs_model;
    }
    
    function get_all_round() view public returns (Model[] memory) {
        return models;
    }
}