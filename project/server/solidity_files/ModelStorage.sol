// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7;

contract ModelStorage {
    string base_model_structure;

    struct Model {
        string ipfs_model;
        string accuracy;
        address author;
    }

    Model[] models;

    constructor(
        string memory ipfs_struct,
        string memory ipfs_weight,
        string memory accuracy_
    ) {
        base_model_structure = ipfs_struct;
        Model memory tmp = Model({
            ipfs_model: ipfs_weight,
            accuracy: accuracy_,
            author: msg.sender
        });
        models.push(tmp);
    }

    function submit_model_weight(
        string memory ipfs_,
        string memory accuracy_
    ) public {
        Model memory submit_ = Model({
            ipfs_model: ipfs_,
            accuracy: accuracy_,
            author: msg.sender
        });

        models.push(submit_);
    }

    function get_model_ipfs() public view returns (string memory) {
        return base_model_structure;
    }

    function get_latest_model_weight_ipfs()
        public
        view
        returns (string memory)
    {
        return models[models.length - 1].ipfs_model;
    }

    function get_all_round() public view returns (Model[] memory) {
        return models;
    }
}
